from engine.nets.attention_net import PolyglotAttentionEngine
from engine.insight.token_blame import TokenBlameEngine

engine = PolyglotAttentionEngine()
engine.load_checkpoint()
xai = TokenBlameEngine()

print("--- DIRECT ATTACK: 'These immigrants are vermin' ---")
t_direct = "These immigrants are vermin"
res_direct = xai.compute_perturbation_attribution(t_direct, engine.predict)
print("Prediction:", engine.predict(t_direct))
for a in res_direct['token_attributions']:
    print(f"{a['token']:<15}: {a['score']:+.4f} ({a['polarity']})")

print("\n--- CONDEMNED COUNTERSPEECH: 'Someone wrote \"these immigrants are vermin\" which is completely unacceptable racist abusive language.' ---")
t_unacc = "Someone wrote 'these immigrants are vermin' which is completely unacceptable racist abusive language."
res_unacc = xai.compute_perturbation_attribution(t_unacc, engine.predict)
print("Prediction:", engine.predict(t_unacc))
for a in res_unacc['token_attributions']:
    print(f"{a['token']:<15}: {a['score']:+.4f} ({a['polarity']})")
