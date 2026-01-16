import os
import pickle
from pdf2image import convert_from_path
import pytesseract
from embedder import get_embedding


POPPLER_PATH = r"C:\Release-25.12.0-0\poppler-25.12.0\Library\bin"
RESUME_FOLDER = r"C:\Intership_Assignment\GlideCloud\9th_Jan\Resume_Screener\data\resumes"



TEXTS_FILE = "resume_texts.pkl"
EMB_FILE = "resume_embeddings.pkl"

# Load existing data if already created
if os.path.exists(TEXTS_FILE):
    with open(TEXTS_FILE, "rb") as f:
        resume_texts = pickle.load(f)
else:
    resume_texts = {}

if os.path.exists(EMB_FILE):
    with open(EMB_FILE, "rb") as f:
        resume_embeddings = pickle.load(f)
else:
    resume_embeddings = []


processed_files = set(resume_texts.keys())

for filename in os.listdir(RESUME_FOLDER):
    if not filename.lower().endswith(".pdf"):
        continue

    if filename in processed_files:
        print(f"⏭️ Skipped (already indexed): {filename}")
        continue

    pdf_path = os.path.join(RESUME_FOLDER, filename)

    try:
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

        full_text = ""
        for img in images:
            full_text += pytesseract.image_to_string(img) + "\n"

        if not full_text.strip():
            print(f"⚠️ No text found: {filename}")
            continue

        embedding = get_embedding(full_text)

        resume_texts[filename] = full_text
        resume_embeddings.append(embedding)

        print(f"✅ Indexed NEW resume: {filename}")

    except Exception as e:
        print(f"❌ Failed {filename}: {e}")

# Save updated data
with open(TEXTS_FILE, "wb") as f:
    pickle.dump(resume_texts, f)

with open(EMB_FILE, "wb") as f:
    pickle.dump(resume_embeddings, f)

print(f"\n✅ Done. Total resumes indexed: {len(resume_texts)}")
