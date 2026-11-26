from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from server.kernel.runtime_config import runtime

router = APIRouter(prefix="/api/preferences", tags=["Preferences"])

@router.get("/")
def load_preferences():
    return {
        "app": runtime.app_config.get("app", {}),
        "compute": {
            "device": runtime.device,
            "threads": runtime.app_config.get("compute", {}).get("num_threads", 4),
            "batch_size": runtime.app_config.get("compute", {}).get("batch_size", 16)
        },
        "reward_weights": runtime.reward_weights,
        "languages": runtime.languages_config.get("languages", {}).get("supported", [])
    }

@router.post("/")
def save_preferences(payload: Dict[str, Any]):
    if "reward_weights" in payload:
        for k, v in payload["reward_weights"].items():
            if k in runtime.reward_weights:
                runtime.reward_weights[k] = float(v)
    return {"status": "updated", "current_reward_weights": runtime.reward_weights}

