from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(chunks: list) -> list:
    """
    Generate embeddings for text chunks
    """
    return model.encode(chunks).tolist()
