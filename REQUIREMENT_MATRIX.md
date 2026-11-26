# Requirements Traceability Matrix (RTM)
## Project: CivilLens: Transparent, Feedback-Tuned Screening of Abusive Online Language
**Instructor / Supervisor:** Dr. Pradeepika Verma

| Ref ID | Official Requirement from Project Specification | Implementation Component | Source File(s) | Verification Method | Status |
|---|---|---|---|---|---|
| **REQ-01** | Binary Classification Target ($f_\theta(x_i) \to y_i \in \{0,1\}$ where 0=Non-hateful, 1=Hateful) | Classification Engine | `engine/baseline/`, `server/contracts/` | Automated unit & integration tests on binary loss & thresholding | VERIFIED |
| **REQ-02** | Multilingual & Code-Mixed Text Processing ($T_i$: English, Hindi, Hinglish, low-resource) | Text Preprocessor & Language Detector | `engine/prep/lexical/`, `engine/locale/` | Script detection tests, transliteration handling, character n-gram tokenization | VERIFIED |
| **REQ-03** | Visual & Meme Input Processing ($V_i$: images, memes, OCR text) | Multimodal Engine & OCR Service | `engine/prep/visual/`, `engine/crossmodal/glyph_reader.py` | EasyOCR text extraction and image tensor validation | VERIFIED |
| **REQ-04** | Contextual Information Modeling ($C_i$: conversational context, thread history, without demographic profiling) | Context Preprocessor & Modality Fusion | `engine/prep/thread/`, `engine/crossmodal/merger.py` | Multi-input forward pass with and without context gating | VERIFIED |
| **REQ-05** | Multimodal Fusion (Joint consideration of text, OCR, visual tokens, and context) | Cross-Attention & Feature-Level Fusion | `engine/crossmodal/merger.py`, `engine/nets/crossmodal_scanner.py` | Ablation experiments comparing text-only vs multimodal inputs | VERIFIED |
| **REQ-06** | Explainable AI (XAI) Grounding (Token-level attribution, visual grounding, natural language explanation) | XAI Engine | `engine/insight/` | Integrated gradients / perturbation attribution, faithfulness perturbation test ($\Delta f(x)$) | VERIFIED |
| **REQ-07** | Human Feedback Collection & Validation | Feedback Manager | `engine/review/`, `server/routes/reviews.py` | Persistent SQLite feedback storage and validation schemas | VERIFIED |
| **REQ-08** | Documented Reward Function $R(x, y, e, f) = \alpha R_{cls} + \beta R_{exp} + \gamma R_{ctx} + \delta R_{fb} - \lambda R_{err}$ | Reward Engine | `engine/incentives/scoring.py` | Unit tests computing multi-objective reward vectors across test instances | VERIFIED |
| **REQ-09** | Feedback-Guided Reward Optimization (Model fine-tuning / preference optimization, versioning, rollback) | Optimization Engine | `engine/tuning/`, `server/routes/tuning.py` | Versioned checkpoints ($v1 \to v2$), held-out test evaluation before/after | VERIFIED |
| **REQ-10** | Bias, Fairness, and Responsible Content Moderation (Disaggregated group metrics, FPR parity, counterspeech) | Fairness & Ethics Engine | `engine/equity/`, `engine/evaluation/` | Disaggregated demographic & language parity evaluation | VERIFIED |
| **REQ-11** | 9 Controlled Research Experiments (Classical vs Transformer, Monolingual vs Multilingual, Multimodal vs Text, Fusion, XAI, Rewards, Scaling, Fairness, Sarcasm) | Experiment Runner | `engine/studies/`, `server/routes/trials.py` | Automated reproducible execution with metric persistence | VERIFIED |
| **REQ-12** | Lumen Design System with Dark Mode (11 dedicated research pages, top-rail layout, squared corners, teal/amber palette) | Frontend Architecture | `web/`, `LUMEN_DESIGN_NOTES.md` | Interactive UI rendering across all 11 pages with persistent dark mode | VERIFIED |
| **REQ-13** | Academic Deliverables: Source Code, ACL Research Paper, and Presentation Slides | Academic Paper & Slides | `manuscript/manuscript.tex`, `manuscript/bibliography.bib`, `pitch/` | Valid LaTeX document and interactive presentation slide deck | VERIFIED |

