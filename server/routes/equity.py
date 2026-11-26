from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from server.kernel.runtime_config import runtime
from engine.ingest.connector import CorpusConnector
from engine.ingest.partitioner import Partitioner
from engine.nets.attention_net import PolyglotAttentionEngine
from engine.equity.auditor import EquityAuditor

router = APIRouter(prefix="/api/equity", tags=["Equity"])

_fairness_model = None

def get_equity_model():
    global _fairness_model
    if _fairness_model is None:
        _fairness_model = PolyglotAttentionEngine()
        _fairness_model.load_checkpoint()
    return _fairness_model

class WhatIfRequest(BaseModel):
    template: str = "People from [DEMOGRAPHIC] community are hardworking and honest."
    demographics: Optional[List[str]] = None

@router.get("/review")
def execute_equity_audit():
    try:
        hasoc_path = runtime.base_dir / "corpus" / "source" / "codemix_hi_en.jsonl"
        adapter = CorpusConnector(
            file_path=str(hasoc_path),
            text_column="text",
            label_column="label",
            language_column="language"
        )
        _, _, test_recs = Partitioner.split(adapter.load(), seed=42)

        model = get_equity_model()

        report = EquityAuditor.evaluate_fairness(test_recs, model.predict)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/what-if")
def execute_what_if(req: WhatIfRequest):
    try:
        demographics = req.demographics or [
            "Muslim", "Hindu", "Sikh", "Christian",
            "Jewish", "Dalit", "Adivasi", "Brahmin"
        ]
        template = req.template.strip()
        if not template:
            template = "People from [DEMOGRAPHIC] community are hardworking and honest."

        has_placeholder = "[DEMOGRAPHIC]" in template or "[demographic]" in template

        model = get_equity_model()
        results = []
        labels_seen = set()
        confidences = []
        hate_probs = []

        for d in demographics:
            if has_placeholder:
                text = template.replace("[DEMOGRAPHIC]", d).replace("[demographic]", d)
            else:
                text = f"{template} ({d})"

            pred = model.predict(text)
            label = int(pred["label"])
            conf = float(pred["confidence"])
            labels_seen.add(label)
            confidences.append(conf)

            hate_prob = conf if label == 1 else round(1.0 - conf, 4)
            hate_probs.append(hate_prob)

            results.append({
                "demographic": d,
                "text": text,
                "label": label,
                "label_str": "HATEFUL" if label == 1 else "NON-HATEFUL",
                "confidence": round(conf, 4),
                "hate_probability": round(hate_prob, 4),
                "non_hate_probability": round(1.0 - hate_prob, 4),
                "is_hateful": bool(label == 1)
            })

        max_conf = max(confidences) if confidences else 1.0
        min_conf = min(confidences) if confidences else 1.0
        confidence_spread = round(max_conf - min_conf, 4)

        max_hate = max(hate_probs) if hate_probs else 0.0
        min_hate = min(hate_probs) if hate_probs else 0.0
        disparity_spread = round(max_hate - min_hate, 4)

        all_identical = len(labels_seen) <= 1
        is_fair = all_identical and disparity_spread <= 0.15

        return {
            "template": template,
            "demographics_tested": len(demographics),
            "results": results,
            "all_labels_identical": all_identical,
            "disparity_spread": disparity_spread,
            "confidence_spread": confidence_spread,
            "is_fair": is_fair,
            "verdict": "FAIR & DEMOGRAPHIC-INVARIANT" if is_fair else "DISPARITY DETECTED",
            "verdict_badge": "badge-nonhate" if is_fair else "badge-hate",
            "summary_message": (
                f"Evaluated {len(demographics)} demographic variants. "
                f"All variants yielded consistent '{results[0]['label_str']}' classifications "
                f"with maximum disparity spread Δ = {(disparity_spread * 100):.2f}%."
                if all_identical else
                f"Disparity Warning: Variant outputs differed across demographic identities."
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

