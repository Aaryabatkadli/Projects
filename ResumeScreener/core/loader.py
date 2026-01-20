import os
import subprocess
from loguru import logger

DATA_DIR = "data/resumes"

def download_kaggle_dataset():
    try:
        # Create directory if not exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)

        # Download dataset
        subprocess.run(
            [
                "kaggle",
                "datasets",
                "download",
                "-d",
                "hadikp/resume-data-pdf",
                "-p",
                DATA_DIR,
                "--unzip"
            ],
            check=True
        )

        logger.info("Kaggle resume dataset downloaded successfully")

    except Exception as e:
        logger.error(f"Dataset download failed: {e}")
        raise
