import faiss
import numpy as np
import os
import pickle

INDEX_DIR = "data/faiss_index"
INDEX_PATH = os.path.join(INDEX_DIR, "resumes.index")
META_PATH = os.path.join(INDEX_DIR, "metadata.pkl")

def build_faiss_index(embeddings_dict):
    if not embeddings_dict:
        raise ValueError("No embeddings found. Check resume parsing.")

    os.makedirs(INDEX_DIR, exist_ok=True)

    names = list(embeddings_dict.keys())
    vectors = np.array(list(embeddings_dict.values()), dtype="float32")

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(names, f)

def search_faiss(query_embedding, embeddings, top_k=5):
    import faiss
    import numpy as np

    dim = len(query_embedding)
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype=np.float32))
    
    D, I = index.search(np.array([query_embedding], dtype=np.float32), top_k)
    
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({"resume": list(resume_texts.keys())[idx], "score": 1 / (1 + score)})
    return results

