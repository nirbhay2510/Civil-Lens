from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ThreadInput(BaseModel):
    thread_history: Optional[List[str]] = Field(default=None, description="Previous messages in thread")
    platform: Optional[str] = Field(default=None, description="Origin platform e.g. twitter, reddit")
    post_type: Optional[str] = Field(default=None, description="Direct post, reply, or quote")

class ScanRequest(BaseModel):
    text: Optional[str] = Field(default="", description="Post text in English, Hindi, or Hinglish")
    image_path: Optional[str] = Field(default=None, description="Optional path or filename of uploaded meme/image")
    image_base64: Optional[str] = Field(default=None, description="Optional base64 image data")
    context: Optional[ThreadInput] = Field(default=None, description="Optional conversation context")
    model_id: Optional[str] = Field(default=None, description="Model to use (defaults to active model)")
    explain: bool = Field(default=True, description="Whether to compute explainability attribution")

class TokenBlame(BaseModel):
    token: str
    score: float
    polarity: str # "positive_evidence" (pushes toward hate) or "negative_evidence" (pushes toward non-hate)

class PixelBlame(BaseModel):
    box: Optional[List[int]] = None # [ymin, xmin, ymax, xmax]
    region_label: Optional[str] = None
    attribution_score: float = 0.0

class NarrationResponse(BaseModel):
    token_attributions: List[TokenBlame] = []
    visual_attributions: List[PixelBlame] = []
    ocr_evidence: Optional[str] = None
    contextual_evidence: Optional[Dict[str, Any]] = None
    natural_language_explanation: str
    faithfulness_score: float # Percentage drop in confidence when top tokens removed
    uncertainty_notes: Optional[str] = None

class ScanResponse(BaseModel):
    prediction_id: str
    predicted_label: int = Field(..., description="0 for Non-Hateful, 1 for Hateful")
    label_name: str = Field(..., description="'NON-HATEFUL' or 'HATEFUL'")
    confidence: float
    model_id: str
    model_version: str
    language_detected: str
    modalities_used: List[str]
    explanation: Optional[NarrationResponse] = None
    created_at: str

