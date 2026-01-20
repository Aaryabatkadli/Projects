# AI Resume Screener (RAG Powered)

An enterprise-grade **AI Resume Screening System** designed for HR teams to automatically shortlist candidates using **LLMs, RAG, OCR, ChromaDB, FAISS, and Streamlit**.

---

## Features

- PDF & image-based resume parsing  
- OCR fallback (Tesseract)  
- Resume chunking  
- Embeddings generation  
- ChromaDB vector storage  
- Optional FAISS hybrid search  
- RAG reasoning using Ollama  
- Resume ranking system  
- Skill & experience filtering  
- Streamlit HR dashboard  
- Logging & error handling  
- Unit tests + HTML report  

---

## Project Structure

```
ResumeScreener/
│
├── app/
│   └── streamlit_app.py
│
├── core/
│   ├── loader.py
│   ├── ocr_engine.py
│   ├── parser.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── ranker.py
│   └── rag_engine.py
│
├── storage/
│   └── chroma/
│
├── tests/
│   ├── test_parser.py
│   ├── test_embeddings.py
│   ├── test_rag.py
│   └── report.html
│
├── logs/
│   └── app.log
│
├── requirements.txt
├── README.md
└── .env
```

---

## Tech Stack

- Python 3.10+
- Streamlit
- ChromaDB
- FAISS
- Ollama (LLM)
- Sentence Transformers
- PyPDF2
- Tesseract OCR
- pytest

---

## Installation

```bash
git clone https://github.com/yourusername/ResumeScreener.git
cd ResumeScreener

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## Environment Setup

Create `.env`

```env
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434

KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key

DATA_DIR=data/resumes
CHROMA_DIR=storage/chroma
LOG_DIR=logs
```

---

## Download Dataset

```bash
python core/loader.py
```

*(Dataset downloaded dynamically – not stored on GitHub)*

---

## Ingest Resumes

```bash
python -m core.ingest_pipeline
```

---

## Run Application

```bash
streamlit run app/streamlit_app.py
```

---

## Generate Test Report

```bash
pytest tests/ --html=tests/report.html --self-contained-html
```

Open:

```
tests/report.html
```

---

## How It Works

1. Downloads Kaggle dataset  
2. Parses resumes  
3. Applies OCR if required  
4. Chunks resume text  
5. Generates embeddings  
6. Stores in ChromaDB  
7. Performs vector search  
8. Ranks resumes  
9. Uses RAG for reasoning  
10. Displays results in Streamlit  

---

## Ranking Criteria

- Skill match  
- Experience match  
- Semantic similarity  

---

## Logging

Logs stored in:

```
logs/app.log
```

---

## Git Ignore

The following are NOT pushed to GitHub:

```
venv/
data/
storage/chroma/
logs/
.env
__pycache__/
```

---

## Security

- Secrets stored in `.env`
- No API keys committed
- Dataset not pushed to GitHub

---

## Author

**Bhuvan Jadhav**

---

## License

MIT License

---

## Support

⭐ Star this repo if you like it!
