import csv
import os
from datetime import datetime

HR_REVIEW_FILE = "hr_review_candidates.csv"
FINALIZED_FILE = "finalized_candidates.csv"

FIELDS = [
    "resume_name",
    "email",
    "phone",
    "skills",
    "experience",
    "score",
    "description",
    "timestamp"
]


def _init_file(path):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()


def save_hr_review(data: dict):
    _init_file(HR_REVIEW_FILE)
    data["timestamp"] = datetime.now().isoformat()

    with open(HR_REVIEW_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(data)


def save_finalized(data: dict):
    _init_file(FINALIZED_FILE)
    data["timestamp"] = datetime.now().isoformat()

    with open(FINALIZED_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(data)
