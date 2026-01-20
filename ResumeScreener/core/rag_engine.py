"""
RAG reasoning engine using Ollama
"""

import os
import ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def rag_reasoning(context: str, question: str) -> str:
    """
    Perform RAG-based reasoning using Ollama
    """

    response = ollama.chat(
        model=os.getenv("OLLAMA_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an HR assistant."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response["message"]["content"]
