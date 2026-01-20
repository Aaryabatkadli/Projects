"""
Unit tests for RAG engine
"""

import sys
import os

# Add project root to path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from core.rag_engine import rag_reasoning


def test_rag_returns_string():
    output = rag_reasoning(
        "Python developer with ML experience",
        "Summarize this resume"
    )

    assert isinstance(output, str)
