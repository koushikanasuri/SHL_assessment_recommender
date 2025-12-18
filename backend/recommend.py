import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "data" / "index" / "faiss.index"
META_PATH = BASE_DIR / "data" / "index" / "meta.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

def recommend(query: str, k: int = 10):
    index = faiss.read_index(str(INDEX_PATH))

    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    query_vector = model.encode(query, normalize_embeddings=True)
    q_vec = np.array([query_vector]).astype("float32")

    scores, indices = index.search(q_vec, k)

    results = []
    seen = set()

    for idx in indices[0]:
        if idx == -1:
            continue
        item = meta[idx]
        url = item.get("url")
        if url and url not in seen:
            results.append(item)
            seen.add(url)
        if len(results) == 10:
            break

    return results
