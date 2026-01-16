from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once
_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    Generate normalized embedding for FAISS L2 search
    """
    emb = _model.encode(text)
    emb = np.array(emb, dtype="float32")

    # Normalize for better L2 distance behavior
    norm = np.linalg.norm(emb)
    if norm > 0:
        emb = emb / norm

    return emb
