import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
import sqlite3
import numpy as np

embedder = SentenceTransformer('all-MiniLM-L6-v2')

class CravingPredictor(nn.Module):
    def __init__(self, input_size=384, hidden_size=128):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, input_size)  # predict next embedding

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

model = CravingPredictor()
model_path = "lisa_model.pt"
try:
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    print("Loaded existing model")
except:
    print("Starting with fresh model")
