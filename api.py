from fastapi import FastAPI
import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI()

# 🔒 Load ONCE
INDEX_PATH = "data/index/faiss.index"
META_PATH = "data/index/meta.json"

index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
@app.get("/recommend")
def recommend(query: str):
    query_vector = model.encode(query, normalize_embeddings=True)
    q_vec = np.array([query_vector], dtype="float32")

    scores, indices = index.search(q_vec, 10)

    results = []
    for idx in indices[0]:
        if idx == -1:
            continue
        results.append(meta[idx])

    return {
        "query": query,
        "results": results
    }
