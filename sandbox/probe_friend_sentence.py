from engine.nets.attention_net import PolyglotAttentionEngine
from engine.baseline.tfidf_linear import TfidfLinearBaseline

t = "you are absolutely stupid and have no idea what you're talking about."

trans = PolyglotAttentionEngine()
trans.load_checkpoint()
print("TRANSFORMER PREDICTION:")
print(trans.predict(t))

classical = TfidfLinearBaseline()
classical.load()
print("\nCLASSICAL TF-IDF PREDICTION:")
print(classical.predict(t))
