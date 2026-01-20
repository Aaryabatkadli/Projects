"""
Persistent ChromaDB vector store
Enterprise-ready implementation
"""

import os
import chromadb
from loguru import logger

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
logger.add("logs/search.log", rotation="1 MB")

# -------------------------------------------------------------------
# Absolute base directory (Windows-safe)
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "storage", "chroma")

os.makedirs(CHROMA_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Persistent Chroma client (SINGLE INSTANCE)
# -------------------------------------------------------------------
_client = chromadb.PersistentClient(path=CHROMA_DIR)

# -------------------------------------------------------------------
# Explicit collection (SINGLE COLLECTION)
# -------------------------------------------------------------------
_resumes_collection = _client.get_or_create_collection(
    name="resumes"
)

# -------------------------------------------------------------------
# Public accessor
# -------------------------------------------------------------------
def get_resumes_collection():
    """
    Returns the persistent resumes collection.
    """
    return _resumes_collection


# -------------------------------------------------------------------
# Store embeddings
# -------------------------------------------------------------------
def store_resume_chunks(chunks, embeddings, metadata):
    """
    Store resume chunks and embeddings persistently.

    Args:
        chunks (list): Text chunks
        embeddings (list): Vector embeddings
        metadata (dict): Resume metadata
    """
    try:
        if not chunks or not embeddings:
            logger.warning("No chunks or embeddings to store.")
            return

        ids = [f"{metadata['filename']}_{i}" for i in range(len(chunks))]

        _resumes_collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=[metadata] * len(chunks),
            ids=ids
        )

        logger.success(
            f"Stored {len(chunks)} chunks for {metadata['filename']}"
        )

    except Exception as e:
        logger.error(f"Failed to store embeddings: {e}")


# -------------------------------------------------------------------
# Search with post-filtering
# -------------------------------------------------------------------
def search_resumes(query, top_k, skills=None, min_exp=None):
    """
    Search resumes using vector similarity + Python filters.

    Args:
        query (str): Job description
        top_k (int): Number of results
        skills (list): Required skills
        min_exp (int): Minimum experience

    Returns:
        dict: Filtered documents & metadata
    """

    try:
        logger.info(
            f"SEARCH | query='{query[:40]}' | skills={skills} | min_exp={min_exp}"
        )

        # ---------------- VECTOR SEARCH ----------------
        results = _resumes_collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        # ---------------- POST FILTERING ----------------
        filtered_docs = []
        filtered_meta = []

        for doc, meta in zip(documents, metadatas):
            if not doc:
                continue

            if skills:
                resume_skills = meta.get("skills","")
                if not any(s in resume_skills for s in skills):
                    continue

            if min_exp and min_exp > 0:
                exp = int(meta.get("experience",0))
                if exp < min_exp:
                    continue

            filtered_docs.append(doc)
            filtered_meta.append(meta)


        logger.success(
            f"SEARCH DONE | results={len(filtered_docs)}"
        )

        return {
            "documents": [filtered_docs],
            "metadatas": [filtered_meta]
        }

    except Exception as e:
        logger.error(f"Search failed: {e}")
        return {"documents": [[]], "metadatas": [[]]}
