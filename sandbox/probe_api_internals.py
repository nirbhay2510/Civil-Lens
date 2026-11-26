import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.routes.scan import get_engines, analyze_content
from server.contracts.scan_models import ScanRequest

classical_clf, transformer_clf = get_engines()
print("transformer_clf:", transformer_clf)
print("is_trained:", transformer_clf.is_trained)
pred = transformer_clf.predict("nigger")
print("Direct predict:", pred)

req = ScanRequest(text="nigger")
api_res = analyze_content(req)
print("analyze_content:", api_res.predicted_label, api_res.label_name, api_res.confidence)
