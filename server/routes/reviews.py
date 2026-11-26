import uuid
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException
from server.contracts.review_models import ReviewCreate, ReviewResponse
from server.store.sqlite_store import open_conn
from engine.review.intake import ReviewIntake
from engine.incentives.scoring import CompositeScorer

router = APIRouter(prefix="/api/reviews", tags=["Reviews & Scoring"])
_reward_calc = CompositeScorer()

@router.post("/", response_model=ReviewResponse)
def post_review(fb: ReviewCreate):
    try:
        res = ReviewIntake.post_review(
            prediction_id=fb.prediction_id,
            is_correct=fb.is_correct,
            suggested_label=fb.suggested_label,
            explanation_rating=fb.explanation_rating,
            flags=fb.flags,
            comment=fb.comment
        )

        # Retrieve prediction to calculate immediate reward
        conn = open_conn()
        p_row = conn.execute("SELECT * FROM predictions WHERE id = ?", (fb.prediction_id,)).fetchone()
        if p_row:
            rew = _reward_calc.calculate_reward(
                predicted_label=p_row["predicted_label"],
                confidence=p_row["confidence"],
                is_correct=fb.is_correct,
                suggested_label=fb.suggested_label,
                explanation_rating=fb.explanation_rating
            )
            rew_id = str(uuid.uuid4())
            conn.execute("""
                INSERT INTO rewards 
                (id, prediction_id, feedback_id, r_classification, r_explanation, r_context, r_feedback, r_error, total_reward, details, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rew_id,
                fb.prediction_id,
                res["feedback_id"],
                rew["r_classification"],
                rew["r_explanation"],
                rew["r_context"],
                rew["r_feedback"],
                rew["r_error"],
                rew["total_reward"],
                json.dumps(rew),
                datetime.now(timezone.utc).isoformat()
            ))
            conn.commit()
        conn.close()

        return ReviewResponse(
            id=res["feedback_id"],
            prediction_id=fb.prediction_id,
            status=res["status"],
            created_at=res["recorded_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_review_records():
    conn = open_conn()
    rows = conn.execute("""
        SELECT f.*, p.input_text, p.predicted_label, p.confidence, p.model_version,
               r.total_reward, r.r_classification, r.r_explanation, r.r_error
        FROM feedback f
        JOIN predictions p ON f.prediction_id = p.id
        LEFT JOIN rewards r ON f.id = r.feedback_id
        ORDER BY f.created_at DESC
        LIMIT 100
    """).fetchall()
    conn.close()

    items = [dict(r) for r in rows]
    total_count = len(items)
    accepted_count = sum(1 for i in items if i["status"] == "accepted")
    rejected_count = total_count - accepted_count

    rewards_list = [i["total_reward"] for i in items if i.get("total_reward") is not None]
    avg_reward = round(sum(rewards_list) / max(1, len(rewards_list)), 4) if rewards_list else 0.0

    return {
        "total_count": total_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "average_reward": avg_reward,
        "records": items
    }
