from model import model, embedder
import torch
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity

def predict_next_cravings(top_k=5):
    conn = sqlite3.connect("cravings.db")
    rows = conn.execute("SELECT text FROM cravings ORDER BY date DESC LIMIT 10").fetchall()
    conn.close()
    if len(rows) < 3:
        return ["I'm still learning your vibes ❤️", "Keep feeding me cravings!"]
    
    recent = [r[0] for r in rows]
    recent_emb = embedder.encode(recent[-1])
    model.eval()
    with torch.no_grad():
        pred_emb = model(torch.tensor(recent_emb).unsqueeze(0).unsqueeze(0)).numpy()
    
    # Find past cravings most similar to prediction
    all_texts = [r[0] for r in conn.execute("SELECT text FROM cravings").fetchall()]
    all_emb = embedder.encode(all_texts)
    sims = cosine_similarity(pred_emb, all_emb)[0]
    top_idx = sims.argsort()[-top_k:][::-1]
    
    return [all_texts[i] for i in top_idx]

if __name__ == "__main__":
    print("Lisa will probably want:")
    for p in predict_next_cravings():
        print("•", p)
