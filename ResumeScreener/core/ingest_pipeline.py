import os
from loguru import logger

from .parser import parse_resume
from .chunker import chunk_text
from .embedder import get_embeddings
from .vector_store import store_resume_chunks

# Dataset path (NOT committed to GitHub)
DATASET_PATH = os.path.join("data", "resumes")


def ingest_dataset():

    if not os.path.exists(DATASET_PATH):
        logger.error(f"Dataset path not found: {DATASET_PATH}")
        return

    files_processed = 0
    chunks_stored = 0

    for root, _, files in os.walk(DATASET_PATH):
        for file in files:

            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(root, file)
            logger.info(f"Ingesting: {file}")
            files_processed += 1

            parsed = parse_resume(pdf_path)
            text = parsed.get("text", "")

            if len(text) < 200:
                logger.warning(f"Skipped (insufficient text): {file}")
                continue

            # Chunk text
            chunks = chunk_text(text)

            # Generate embeddings
            embeddings = get_embeddings(chunks)

            metadata = {
                "filename": file,
                "source": "kaggle",
                "doc_type": "resume"
            }

            # Store in vector DB
            store_resume_chunks(chunks, embeddings, metadata)
            chunks_stored += len(chunks)

    logger.success(
        f"Ingestion completed | Files: {files_processed} | Chunks: {chunks_stored}"
    )


if __name__ == "__main__":
    ingest_dataset()
