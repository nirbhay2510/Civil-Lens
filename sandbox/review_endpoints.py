import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

print('=== 1. Core Endpoints ===')
core_eps = [
    '/', '/pulse', '/api/briefs/digest', '/api/briefs/manuscript',
    '/api/corpora/', '/api/engines/', '/api/tuning/log',
    '/api/equity/review', '/api/trials/', '/api/preferences/', '/api/reviews/'
]
for ep in core_eps:
    r = client.get(ep)
    print(f'GET {ep:32} -> {r.status_code}')

print('\n=== 2. Detection Endpoint ===')
# Test text-only civil detection
r_det = client.post('/api/scan/analyze', json={'text': 'Hello world, have a good day.', 'explain': True})
d1 = r_det.json()
print(f"POST /api/scan/analyze (civil)   -> {r_det.status_code}, label={d1.get('label_name')}, conf={d1.get('confidence')}")

# Test hate detection
r_hate = client.post('/api/scan/analyze', json={'text': 'These vermin immigrants are destroying our country.', 'explain': True})
d2 = r_hate.json()
print(f"POST /api/scan/analyze (hate)    -> {r_hate.status_code}, label={d2.get('label_name')}, conf={d2.get('confidence')}")

# Test negated slur detection (Way 1)
r_neg = client.post('/api/scan/analyze', json={'text': 'These immigrants are not vermin destroying our country.', 'explain': True})
d_neg = r_neg.json()
print(f"POST /api/scan/analyze (negated) -> {r_neg.status_code}, label={d_neg.get('label_name')}, conf={d_neg.get('confidence')}")

# Test classical model
r_class = client.post('/api/scan/analyze', json={'text': 'Test text for classical baseline', 'model_id': 'classical-tfidf-svm', 'explain': False})
d3 = r_class.json()
print(f"POST /api/scan/analyze (classical) -> {r_class.status_code}, label={d3.get('label_name')}")

# Test LLM reasoner model
r_llm = client.post('/api/scan/analyze', json={'text': 'You are stupid and bad', 'model_id': 'llm-structured-reasoner-v1', 'explain': False})
d4 = r_llm.json()
print(f"POST /api/scan/analyze (llm)       -> {r_llm.status_code}, label={d4.get('label_name')}")

print('\n=== 3. Fairness Counterfactual Probe ===')
r_probe = client.post('/api/equity/probe', json={'template': 'People from [DEMOGRAPHIC] community are hardworking.'})
print(f"POST /api/equity/probe              -> {r_probe.status_code}, variance={r_probe.json().get('variance')}")

print('\n=== 4. Reward Simulation ===')
r_sim = client.post('/api/tuning/preview-score', json={
    'predicted_label': 1, 'confidence': 0.95, 'is_correct': True, 'faithfulness_score': 0.8
})
print(f"POST /api/tuning/preview-score -> {r_sim.status_code}, total_reward={r_sim.json().get('total_reward')}")

print('\n=== 5. Dataset Inspection ===')
r_ds_insp = client.get('/api/corpora/codemix_hi_en/inspect?limit=5')
print(f"GET /api/corpora/.../inspect         -> {r_ds_insp.status_code}, total={r_ds_insp.json().get('total_samples')}")

print('\n=== 6. Settings Update ===')
r_settings_get = client.get('/api/preferences/')
print(f"GET /api/preferences/                    -> {r_settings_get.status_code}")
r_settings_post = client.post('/api/preferences/', json={
    'reward_weights': {'alpha': 0.35, 'beta': 0.25, 'gamma': 0.15, 'delta': 0.25, 'lambda_penalty': 0.50}
})
print(f"POST /api/preferences/                   -> {r_settings_post.status_code}")

print('\n=== 7. Static and Presentation Serving ===')
r_idx = client.get('/')
print(f"GET /                                 -> {r_idx.status_code}, length={len(r_idx.content)}")
r_pres = client.get('/pitch/index.html')
print(f"GET /pitch/index.html          -> {r_pres.status_code}, length={len(r_pres.content)}")
r_css = client.get('/static/css/lumen.css')
print(f"GET /static/css/lumen.css     -> {r_css.status_code}, length={len(r_css.content)}")
