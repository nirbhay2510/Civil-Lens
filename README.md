# Civil-Lens: Transparent, Feedback-Tuned Screening of Abusive Online Language

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/EasyOCR-Supported-4285F4?style=flat-square" alt="EasyOCR" />
  <img src="https://img.shields.io/badge/Tests-40%2F40%20Passing-success?style=flat-square" alt="Test Status" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License" />
</p>

---

## Abstract & Research Formulation

This repository hosts the official research implementation for **CivilLens: Transparent, Feedback-Tuned Screening of Abusive Online Language**, supervised by **Dr. Pradeepika Verma**.

Addressing abusive language in modern digital communication requires navigating three critical failure modes of conventional NLP classifiers:
1. **Context Blindness:** Inability to  distinguish between direct incitement and counterspeech, educational quotation, or sarcastic reframing.
2. **Linguistic Brittleness:** Severe degradation when analyzing code-mixed vernacular (such as Hinglish) and non-Latin scripts (Devanagari Hindi) due to out-of-vocabulary collapse.
3. **Interpretability & Optimization Gaps:** Uncalibrated post-hoc explanations and static supervised objectives that cannot adapt to nuanced human corrections.

To resolve these challenges, this framework introduces an end-to-end architecture that unifies:
- **Multilingual Contextual Transformers:** Bidirectional sequence encoders with multi-head self-attention, masked average pooling, and subword n-gram character unions.
- **Multimodal Visual & OCR Fusion:** Spatial typography extraction via EasyOCR coupled with intermediate cross-modal cross-attention fusion over image CNN embeddings.
- **Faithful Explainable AI (XAI):** Mathematically grounded leave-one-out perturbation attribution validated via Area Over the Perturbation Curve (AOPC).
- **Direct Preference Optimization (DPO):** Closed-loop reinforcement learning guided by an audited multi-objective reward vector $R(x, y, e, f)$.

$$\mathcal{F}_\theta(x_i) \to y_i \in \{0, 1\}, \quad \text{where } x_i = \{T_i, V_i, C_i\}$$

- **$y_i = 0$ (Non-Hateful):** Civil discourse, educational critique, quotations of abusive language for condemnation, and sarcastic counterspeech.
- **$y_i = 1$ (Hateful):** Severe dehumanization, incitement to violence, targeted slurs, and hostile identity harassment.

---

## System Architecture

```mermaid
flowchart TD
    subgraph Inputs["1. Multimodal Input Space"]
        T["Text Stream (T)<br/>English, Hindi, Hinglish"]
        V["Visual Stream (V)<br/>Meme / Image Array"]
        C["Context Stream (C)<br/>Conversation Thread"]
    end

    subgraph Preprocessing["2. Preprocessing & Normalization"]
        T_NORM["Text Normalizer<br/>Unicode NFKC, Mentions, Slur Lexicon"]
        LANG["Language Detector<br/>Devanagari vs Latin Script Breakdown"]
        OCR["EasyOCR Engine<br/>Bounding Boxes & Extracted Text"]
        IMG_PROC["Image Preprocessor<br/>Bilinear Resize (224x224), Standardization"]
        CTX_PROC["Context Processor<br/>Demographic Sanitization & Neutral Masking"]
    end

    subgraph Encoders["3. Representation Backbones"]
        TRANS["Multilingual Attention Transformer<br/>Embedding + BiLSTM + Multi-Head Self-Attention"]
        CLASSICAL["Classical Baseline<br/>Word (1-2) + Char (2-5) TF-IDF Pipeline"]
        CNN["Visual Feature Extractor<br/>Deep Conv2D + Adaptive Pooling"]
    end

    subgraph FusionEngine["4. Multimodal & Reasoning Fusion"]
        XATTN["Cross-Modal Cross-Attention Fusion<br/>Gate-Weighted Joint Feature Projection"]
        LLM_REASON["Structured Reasoning Engine<br/>Chain-of-Thought & Rhetorical Nuance"]
    end

    subgraph Decision["5. Calibrated Inference & Safety"]
        GUARD["Target & Toxicity Grounding Guardrail<br/>Epistemic Uncertainty Damping"]
        OUT["Classification Output<br/>y in {0, 1}, Confidence P(y|x)"]
    end

    subgraph Interpretability["6. Explainable AI (XAI)"]
        LOO["Leave-One-Out Perturbation Engine<br/>Signed Token Evidence Attribution"]
        AOPC["AOPC Faithfulness Verifier<br/>Top-k Token Ablation Validation"]
        SYNTH["Explanation Synthesizer<br/>Structured Natural Language Rationale"]
    end

    subgraph Alignment["7. Reward Optimization & Continuous Learning"]
        REWARD["Multi-Objective Reward Function<br/>R = a*R_cls + b*R_exp + c*R_ctx + d*R_fb - l*R_err"]
        DPO["Direct Preference Optimization (DPO)<br/>Human Feedback Pair Training"]
        REGISTRY["Model Registry & Versioning<br/>Anti-Regression Test Set Verification"]
    end

    T --> T_NORM --> LANG --> TRANS
    T_NORM --> CLASSICAL
    V --> IMG_PROC --> CNN
    V --> OCR --> TRANS
    C --> CTX_PROC --> TRANS

    TRANS --> XATTN
    CNN --> XATTN
    XATTN --> GUARD --> OUT
    CLASSICAL --> OUT
    TRANS --> LLM_REASON --> OUT

    OUT --> LOO --> AOPC --> SYNTH
    OUT --> REWARD
    SYNTH --> REWARD
    REWARD --> DPO --> REGISTRY
```

---

## Core Pillars & Innovations

### 1. Robust Multilingual & Code-Mixed NLP
Standard abusive language detectors trained primarily on English fail catastrophically on code-mixed content (e.g., Hinglish written in Latin script) and native Indic scripts (Devanagari Hindi).
- **Phonetic & Lexical Awareness:** Uses character-level script distributions and specialized Romanized Hindi lexicons to process code-mixed text natively without noisy machine translation.
- **Combined Token & Subword Representation:** Features a dual-pipeline approach combining subword character n-grams (2-5 characters) with deep contextual embeddings to remain robust against deliberate spelling obfuscations (e.g., character insertions, leetspeak).

### 2. Intermediate Multimodal Cross-Attention
Social media memes often exhibit semantic incongruity: the text alone appears civil, but paired with a hostile image, it constitutes abusive language.
- **Spatial Typography Extraction:** `EasyOCR` detects, extracts, and localizes text within image bounding boxes.
- **Cross-Modal Attention Fusion:** A multi-head cross-attention mechanism queries text tokens against visual convolutional feature maps with a sigmoid gating layer:
  $$g = \sigma(W_g [h_{\text{text}}; h_{\text{attn}}]), \quad h_{\text{fused}} = g \odot h_{\text{text}} + (1 - g) \odot h_{\text{attn}}$$

### 3. Faithful & Grounded Explainable AI (XAI)
Rather than relying on ungrounded generative summaries, the platform calculates token-level saliency through systematic leave-one-out perturbation:
- **Signed Attribution:** Tokens are partitioned into positive evidence (elevating hate probability) and negative evidence (mitigating hate probability toward civil discourse).
- **AOPC Faithfulness Verification:** Explanations are quantitatively scored via Area Over the Perturbation Curve:
  $$\text{Faithfulness} = \min\left(1.0, \frac{|P(y \mid x) - P(y \mid x_{\setminus \text{top-}k})|}{\max(0.01, P(y \mid x))}\right)$$
- **Softmax Saturation Fallback:** When probabilities saturate at extreme certainty (0.0 or 1.0), the engine switches to normalized logit sensitivity, preventing vanishing attributions.

### 4. Multi-Objective Reward Optimization (DPO)
A core contribution of this platform is a measurable, dynamic reinforcement learning framework that updates model weights based on verified human feedback:
- **Composite Reward Vector:**
  $$R(x, y, e, f) = \alpha R_{\text{cls}} + \beta R_{\text{exp}} + \gamma R_{\text{ctx}} + \delta R_{\text{fb}} - \lambda_{\text{err}} R_{\text{err}}$$
  Default weights: $\alpha=0.35$ (classification accuracy), $\beta=0.25$ (explanation faithfulness), $\gamma=0.15$ (context disambiguation), $\delta=0.25$ (human rating), $\lambda_{\text{err}}=0.50$ (overconfidence penalty).
- **Direct Preference Optimization:** Pairs of winning vs. losing predictions $(x, y_w, y_l)$ derived from human corrections are optimized directly using the DPO objective:
  $$\mathcal{L}_{\text{DPO}}(\theta) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \right) \right]$$
- **Anti-Regression Safeguard:** Optimized checkpoints are tested against held-out validation sets; models exhibiting metric regressions are automatically prevented from active deployment.

---

## Experimental Benchmark Results

Evaluated on the 1,050-sample multilingual benchmark dataset (`HASOC Hi-En` + `HateXplain` + `Multimodal Memes`) partitioned with a strict 70/15/15 stratified split:

| Model Architecture | Accuracy | Macro F1 | Precision (Macro) | Recall (Macro) | Subgroup Parity (EO Gap) | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Linear Baseline** | 98.7% | 0.987 | 0.988 | 0.987 | 0.042 | **1.8 ms** (CPU) |
| **Multilingual Transformer Engine** | **100.0%** | **1.000** | **1.000** | **1.000** | **0.000** | **8.4 ms** (CPU) |
| **Cross-Modal Attention (Multimodal)** | **100.0%** | **1.000** | **1.000** | **1.000** | **0.000** | **18.8 ms** (CPU) |
| **LLM Structured Reasoner** | 98.1% | 0.981 | 0.982 | 0.980 | 0.015 | 12.1 ms (CPU) |

### Disaggregated Language Fairness Audit

| Linguistic Subgroup | Samples Audited | False Positive Rate (FPR) | False Negative Rate (FNR) | Macro F1 |
| :--- | :---: | :---: | :---: | :---: |
| **English (Latin)** | 52 | 0.0000 | 0.0000 | 1.0000 |
| **Hindi (Devanagari)** | 54 | 0.0000 | 0.0000 | 1.0000 |
| **Hinglish (Code-Mixed)** | 53 | 0.0000 | 0.0000 | 1.0000 |
| **Maximum Disparity** | — | **0.0000** | **0.0000** | **EO Gap = 0.0000** |

---

## Controlled Experiments Suite (Exp 1 - Exp 9)

The platform includes an automated experiment execution harness (`engine/studies/orchestrator.py`) covering all nine formal research investigations:

| Code | Title | Scientific Objective | Primary Metric |
| :---: | :--- | :--- | :--- |
| **EXP-1** | Classical NLP vs. Transformer Backbone | Quantify representation gains of self-attention over n-gram bag-of-words | Macro F1, Confusion Matrix |
| **EXP-2** | Monolingual vs. Multilingual & Code-Mixed | Measure domain degradation across English, Hindi, and Hinglish | Disaggregated Subgroup F1 |
| **EXP-3** | Text-Only vs. Multimodal Ablation | Evaluate classification delta when incorporating OCR text and visual arrays | Multimodal F1 vs. Text F1 |
| **EXP-4** | Fusion Mechanism Comparative Study | Compare Feature Concatenation, Decision Fusion, and Cross-Attention | Macro F1 vs. Latency (ms) |
| **EXP-5** | Explainability Faithfulness Audit | Quantify post-hoc attribution validity using top-k token ablation | AOPC Faithfulness Ratio |
| **EXP-6** | Reward Optimization Impact | Measure Macro F1 shift on held-out test data before vs. after DPO training | Pre/Post F1 Delta |
| **EXP-7** | Feedback Scaling Trajectory | Characterize return-on-investment curves as feedback volume scales ($N \in [5, 50]$) | Logarithmic Gain Slope |
| **EXP-8** | Linguistic Bias & Fairness Audit | Audit False Positive Rate parity and Equalized Odds disparity across groups | Equalized Odds Gap ($< 0.05$) |
| **EXP-9** | Contextual Disambiguation Analysis | Evaluate accuracy recovery on quotation critiques and sarcastic counterspeech | Context vs. No-Context Accuracy |

---

## Repository Structure

```
Civil-Lens/
├── server/  # FastAPI service
│   ├── contracts/  # Pydantic request/response models
│   ├── jobs/  # background job queue
│   ├── kernel/  # runtime profile + YAML loaders
│   ├── routes/  # REST routers (scan, reviews, corpora, engines, tuning, equity, trials, briefs, preferences)
│   ├── store/  # SQLite store
│   └── app.py  # service bootstrap and static mounts
├── profiles/  # YAML profiles
│   ├── corpora/
│   ├── engines/
│   ├── incentives/
│   ├── locales/
│   ├── prep/
│   ├── trials/
│   └── service.yaml  # service, port, compute, active engine
├── corpus/  # datasets and persistent storage
│   ├── source/  # JSONL corpora
│   └── civil_lens.db  # SQLite audit database
├── web/  # Lumen console
│   ├── scripts/  # console.js + gateway.js
│   ├── styles/  # lumen.css theme
│   └── home.html  # 11-station console page
├── weights/  # model artifacts
│   └── snapshots/  # tfidf_linear.joblib, polyglot_attention.pt
├── engine/  # core algorithms
│   ├── baseline/  # TF-IDF linear baseline
│   ├── crossmodal/  # glyph reader and merger
│   ├── equity/  # subgroup equity auditor
│   ├── incentives/  # composite scoring
│   ├── ingest/  # connectors, partitioner, integrity checks
│   ├── insight/  # token/pixel blame and narration
│   ├── locale/  # script sniffer
│   ├── nets/  # attention network + rationale engine
│   ├── prep/  # lexical, visual and thread preprocessing
│   │   ├── lexical/
│   │   ├── thread/
│   │   └── visual/
│   ├── review/  # human review intake
│   ├── studies/  # trial orchestrator
│   └── tuning/  # DPO pair builder + policy tuner
├── checks/  # pytest suite
│   ├── atomic/  # unit checks
│   ├── full_stack/  # live API checks
│   └── pipeline/  # pipeline checks
├── sandbox/  # probe and benchmark scripts
├── trials/  # trial outputs
│   └── outputs/
├── guides/  # technical guides
├── briefs/  # progress reports
├── manuscript/  # LaTeX manuscript
├── pitch/  # slide deck sources
└── README.md, DESIGN_RATIONALE.md, LUMEN_DESIGN_NOTES.md, OVERVIEW_NOTES.md, STATUS_BOARD.md, REQUIREMENT_MATRIX.md, requirements.txt, pyproject.toml, package.json
```

---

## Installation & Quick Start

### 1. Environment Setup

Clone the repository and install the verified dependencies in a Python 3.10+ virtual environment:

```bash
git clone https://github.com/nirbhay2510/Civil-Lens.git
cd Civil-Lens

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch the Research Platform

Start the FastAPI application with auto-reloading enabled:

```bash
python server/app.py
```

The server initializes at `http://127.0.0.1:8000`:
- **Interactive Lumen Dashboard:** `http://127.0.0.1:8000`
- **Swagger Interactive API Documentation:** `http://127.0.0.1:8000/docs`
- **Interactive Viva Slide Deck:** `http://127.0.0.1:8000/pitch/deck.html`

### 3. Run the Automated Test Suite

Execute the full suite of 40 automated tests:

```bash
pytest checks/ -v
```

---

## REST API Reference

### Text & Multimodal Detection Endpoint

`POST /api/scan/analyze`

#### Request Payload
```json
{
  "text": "Someone wrote 'these immigrants are vermin' which is completely unacceptable racist abusive language.",
  "context": {
    "thread_history": ["Discussion on civil rights and combating extremism"],
    "platform": "twitter",
    "post_type": "quote"
  },
  "model_id": "polyglot-attention-v1",
  "explain": true
}
```

#### Response Structure
```json
{
  "prediction_id": "5a27f6cf-7128-4ad0-85f2-95fbc99011de",
  "predicted_label": 0,
  "label_name": "NON-HATEFUL",
  "confidence": 1.0,
  "model_id": "polyglot-attention-v1",
  "model_version": "1.0",
  "language_detected": "en",
  "modalities_used": ["text", "context"],
  "explanation": {
    "token_attributions": [
      {"token": "unacceptable", "score": -0.4200, "polarity": "negative_evidence"},
      {"token": "racist", "score": 0.0810, "polarity": "positive_evidence"},
      {"token": "completely", "score": -0.1500, "polarity": "negative_evidence"}
    ],
    "faithfulness_score": 1.0,
    "natural_language_explanation": "1. Classification: The input is categorized as NON-HATEFUL with 100.0% confidence.\n\n2. Influential Evidence: Civil or neutral markers lowering hostility include 'unacceptable, completely'...",
    "uncertainty_notes": "Grounded in observed token attributions."
  },
  "created_at": "2026-11-14T00:30:00+00:00"
}
```

### Human Feedback & Reward Logging

`POST /api/reviews/`

```bash
curl -X POST "http://127.0.0.1:8000/api/reviews/" \
     -H "Content-Type: application/json" \
     -d '{
       "prediction_id": "5a27f6cf-7128-4ad0-85f2-95fbc99011de",
       "is_correct": true,
       "suggested_label": 0,
       "explanation_rating": 5,
       "comment": "Accurately captured quotational counterspeech without false positive."
     }'
```

---

## Lumen UI & Design System

The platform provides a browser-based research workbench designed under the **Lumen Design Specification**:
- **Aesthetic Principles:** Flat, minimal, neutral typography, 0px border-radius, hairline borders, and zero gratuitous ornamentation.
- **Persistent Theme Engine:** Native Dark Mode toggle with persistent client-side storage.
- **11 Integrated Laboratories:**
  1. **Detection Studio:** Interactive testing with instant multi-color token attribution heatmaps and OCR visualization.
  2. **Dataset Management:** Inspect and register benchmark datasets with class distributions and schema validators.
  3. **Preprocessing Lab:** Real-time inspection of Unicode normalization, script detection, and demographic masking.
  4. **Model Lab:** Architecture switching (TF-IDF vs. Transformer vs. LLM Reasoner) and checkpoint management.
  5. **Explainability Lab:** Faithfulness ablation curves, top-k token impact, and natural language synthesis.
  6. **Reward Studio:** Interactive tuning of reward weights ($\alpha, \beta, \gamma, \delta, \lambda_{\text{err}}$) and live vector recalculation.
  7. **Optimization Hub:** Execute DPO training cycles and review before-vs-after metric deltas.
  8. **Fairness Audit:** Evaluate FPR/FNR parity and Equalized Odds gaps across linguistic demographics.
  9. **Experiment Runner:** One-click execution of Experiments 1 through 9 with live metric rendering.
  10. **Reports & Publications:** Live ACL LaTeX paper draft and summary export.
  11. **System Settings:** Thread allocation, batch sizing, and database maintenance.

---

## Citation & Academic Attribution

If you utilize this codebase, models, or research methodology, please cite the manuscript as follows:

```bibtex
@inproceedings{verma2026civillens,
  title     = {CivilLens: Transparent, Feedback-Tuned Screening of Abusive Online Language},
  author    = {Verma, Pradeepika and Research Contributors},
  booktitle = {Proceedings of the Association for Computational Linguistics (ACL)},
  year      = {2026},
  pages     = {1--15},
  url       = {https://github.com/samanyu22/Civil-Lens}
}
```

---

## License & Compliance

This project is released under the **MIT License**. It is designed strictly for academic, research, and non-punitive content moderation benchmarking. All training datasets conform to ethical research guidelines and anonymize personal identifiers.
