"""
Unit tests for embedding module
"""

import sys
import os

# Add project root to path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from core.embedder import get_embeddings


def test_embeddings_output_type():
    chunks = ["hello world", "resume text"]
    emb = get_embeddings(chunks)

    assert isinstance(emb, list)
    assert len(emb) == 2


def test_embeddings_vector_size():
    chunks = ["test"]
    emb = get_embeddings(chunks)

    assert isinstance(emb[0], list)
    assert len(emb[0]) > 0
