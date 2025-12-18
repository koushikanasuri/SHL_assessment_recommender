import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# ---------- CONFIG ----------
INPUT_PATH = "data/raw/shl_assessments.json"
INDEX_DIR = "data/index"
INDEX_PATH = "data/index/faiss.index"
META_PATH = "data/index/meta.json"

os.makedirs(INDEX_DIR, exist_ok=True)

# ---------- MODEL ----------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- HELPER ----------
def infer_test_type(text: str):
    text = text.lower()
    types = []

    if any(k in text for k in ["cognitive", "aptitude", "ability", "reasoning"]):
        types.append("Cognitive")

    if any(k in text for k in ["personality", "opq", "behavior", "behaviour"]):
        types.append("Personality")

    if any(k in text for k in ["coding", "programming", "software", "developer"]):
        types.append("Technical")

    if any(k in text for k in ["sales", "leadership", "manager", "management"]):
        types.append("Behavioral")

    return list(set(types))
def is_individual_test(item):
    name = (item.get("name") or "").lower()
    url = (item.get("url") or "").lower()

    banned_keywords = [
        "report",
        "solution",
        "package",
        "job",
        "bundle",
        "profile",
        "suite"
    ]

    for k in banned_keywords:
        if k in name or k in url:
            return False

    return True

# ---------- MAIN ----------
def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    meta = []
    #kept=skipped=0
    for item in data:
        if not is_individual_test(item):
            skipped+=1
            continue
        kept+=1
        name = item.get("name", "")
        desc = item.get("description", "")

        full_text = f"{name} {desc}"
        texts.append(full_text)

        meta.append({
            "name": name,
            "url": item.get("url"),
            "description": desc,
            "duration": None,
            "remote_support": None,
            "adaptive_support": None,
            "test_type": infer_test_type(full_text)
        })

    print("Encoding texts...")
    vectors = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    vectors = np.array(vectors, dtype="float32")

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    '''print("FAISS index built successfully.")
    print(f"Kept {kept} individual tests, skipped {skipped}")'''

if __name__ == "__main__":
    main()


