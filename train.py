from model import model, embedder
import torch
import sqlite3
from torch.utils.data import Dataset, DataLoader
import numpy as np

class CravingDataset(Dataset):
    def __init__(self):
        conn = sqlite3.connect("cravings.db")
        rows = conn.execute("SELECT text FROM cravings ORDER BY date").fetchall()
        conn.close()
        self.texts = [r[0] for r in rows]
        if len(self.texts) < 5:
            return
        self.embeds = embedder.encode(self.texts, convert_to_tensor=True)

    def __len__(self): return max(0, len(self.texts) - 1)
    def __getitem__(self, i): return self.embeds[i], self.embeds[i+1]

dataset = CravingDataset()
if len(dataset) > 0:
    loader = DataLoader(dataset, batch_size=4, shuffle=True)
    opt = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.MSELoss()
    
    model.train()
    for epoch in range(20):
        for x, y in loader:
            opt.zero_grad()
            pred = model(x.unsqueeze(1))
            loss = loss_fn(pred, y)
            loss.backward()
            opt.step()
    
    torch.save(model.state_dict(), "lisa_model.pt")
    print("Model retrained!")
