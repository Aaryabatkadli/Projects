# preprocess.py
import os
from parse_resume import parse_resume
from vector_store import add_resume, save_index, init_index
from embedder import get_batch_embeddings

RESUME_FOLDER = "data/Resumes"

def get_all_resume_paths(folder):
    
    paths = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith((".pdf", ".docx", ".txt")):
                paths.append(os.path.join(root, f))
    return paths

def main():
    all_files = get_all_resume_paths(RESUME_FOLDER)
    print(f"Found {len(all_files)} resumes.")
    
    all_texts = []
    for i, file_path in enumerate(all_files, 1):
        text = parse_resume(file_path)
        if text:
            all_texts.append(text)
        else:
            print(f"⚠️ Failed to extract text from {file_path}")
        if i % 100 == 0:
            print(f"Processed {i}/{len(all_files)} resumes...")
    
    if not all_texts:
        print("❌ No resume text could be extracted. Cannot build index.")
        return
    
    print("✅ Successfully extracted text from resumes. Generating embeddings...")
    
    # Batch embeddings for efficiency
    embeddings = get_batch_embeddings(all_texts, batch_size=50, delay=1)
    
    init_index(sample_text=all_texts[0])
    
    for text, emb in zip(all_texts, embeddings):
        add_resume(text, embedding_override=emb)
    
    save_index()
    print("✅ All resumes processed and FAISS index saved.")

if __name__ == "__main__":
    main()
