import re
import pdfplumber

def parse_resume(uploaded_file):
    """
    Extract resume text + structured info
    """

    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Email
    email = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        text
    )

    # Phone
    phone = re.findall(r"\+?\d[\d\s\-]{8,15}\d", text)

    # Skills
    skills_db = [
        "python", "java", "sql", "ml", "ai", "docker",
        "kubernetes", "aws", "gcp", "terraform",
        "react", "node", "flask", "django"
    ]

    skills = [s for s in skills_db if s in text.lower()]

    # Experience
    exp_years = 0
    exp_match = re.findall(r"(\d+)\+?\s+years", text.lower())
    if exp_match:
        exp_years = max(map(int, exp_match))

    meta = {
        "email": email[0] if email else "Not found",
        "phone": phone[0] if phone else "Not found",
        "skills": list(set(skills)),
        "experience": exp_years
    }

    return text, meta
