import re
from PyPDF2 import PdfReader
from loguru import logger
from .ocr_engine import extract_text_from_image_pdf

SKILLS = [
    "python","aws","docker","kubernetes","ml","nlp",
    "sql","java","react","node","linux","git"
]

def extract_skills(text):
    text = text.lower()
    found = [s for s in SKILLS if s in text]
    return list(set(found))

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s+years?', text.lower())
    if matches:
        return max(map(int, matches))
    return 0

def parse_resume(pdf_path: str) -> dict:
    try:
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if len(text.strip()) < 100:
            logger.info(f"OCR fallback used: {pdf_path}")
            text = extract_text_from_image_pdf(pdf_path)

        skills = extract_skills(text)
        exp = extract_experience(text)

        return {
            "text": text,
            "skills": skills,
            "experience": exp
        }

    except Exception as e:
        logger.error(f"Parsing failed for {pdf_path}: {e}")
        return {"text": "", "skills": [], "experience": 0}
