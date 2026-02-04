import pytesseract
from pdf2image import convert_from_path
from loguru import logger


def extract_text_from_image_pdf(pdf_path: str) -> str:
    """
    Extract text from scanned/image-based PDFs using OCR
    """

    try:
        pages = convert_from_path(pdf_path)
        text = ""

        for page in pages:
            text += pytesseract.image_to_string(page)

        return text

    except Exception as e:
        logger.error(f"OCR failed for {pdf_path}: {e}")
        return ""
