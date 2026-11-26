import io
import base64
import torch
from PIL import Image
from engine.prep.lexical.cleaner import TextCleaner
from engine.prep.visual.pixel_prep import PixelPrep
from engine.crossmodal.merger import CrossModalScanner
from server.contracts.scan_models import ScanRequest
from engine.locale.script_sniffer import ScriptSniffer

def test_devanagari_token_unification():
    norm = TextCleaner()
    tokens = norm.tokenize_words("नमस्ते दोस्तों ये गद्दार हैं!")
    assert "नमस्ते" in tokens
    assert "गद्दार" in tokens
    assert "दोस्तों" in tokens
    # Ensure virama and matras are not loose punctuation tokens
    assert "्" not in tokens
    assert "ा" not in tokens

def test_image_preprocessor_raw_base64_support():
    img = Image.new("RGB", (64, 64), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    raw_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    prep = PixelPrep()
    loaded = prep.load_image(raw_b64)
    assert loaded.size == (64, 64)

def test_multimodal_cross_attention_integration():
    detector = CrossModalScanner(dim=128, text_in_dim=256, fusion_type="cross_attention")
    detector.eval()
    t_feat = torch.randn(1, 256)
    img_tensor = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        logits = detector(t_feat, img_tensor)
    assert logits.shape == (1, 2)

def test_detection_request_image_only_support():
    req = ScanRequest(image_path="corpus/source/visuals/card_counter.png")
    assert req.text == ""
    assert req.image_path == "corpus/source/visuals/card_counter.png"

def test_hinglish_phonetic_elongation_matching():
    res = ScriptSniffer.detect("bhaaaai ye deshdrohi log hai")
    assert res["is_code_mixed"] is True
    assert res["language"] == "hi-en"

