import streamlit as st
import pickle
import numpy as np
import faiss
import re

from embedder import get_embedding
from gpt_analysis import analyze_resume


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.markdown(
    "<h1 style='text-align:center;color:#6a00ff;'>AI Resume Screener</h1>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

min_score = st.sidebar.slider("Minimum Match Score", 0.0, 1.0, 0.3, 0.05)
min_experience = st.sidebar.slider("Minimum Experience (Years)", 0, 30, 0)
skill_filter = st.sidebar.text_input("Required Skill (optional)", placeholder="python, sql")

# ---------------- UTIL FUNCTIONS ----------------
def extract_candidate_info(text):
    # Email
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email[0] if email else "Not found"

    # Phone
    phone = re.findall(r"\+?\d[\d\s\-]{8,15}\d", text)
    phone = phone[0] if phone else "Not found"

    # Name (simple heuristic: first non-empty line)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    name = lines[0] if lines else "Not found"

    # Skills
    skills_db = [
        "python","java","sql","ml","ai","docker","aws",
        "kubernetes","react","node","flask","django"
    ]
    skills = [s for s in skills_db if s in text.lower()]

    # Experience
    experience = 0
    match = re.findall(r"(\d+)\+?\s+years", text.lower())
    if match:
        experience = max(map(int, match))

    return name, email, phone, skills, experience


# ---------------- LOAD DATA ----------------
@st.cache_resource
def load_data():
    with open("resume_texts.pkl", "rb") as f:
        resume_texts = pickle.load(f)

    with open("resume_embeddings.pkl", "rb") as f:
        resume_embeddings = pickle.load(f)

    emb = np.array(resume_embeddings, dtype=np.float32)
    index = faiss.IndexFlatL2(emb.shape[1])
    index.add(emb)

    return resume_texts, list(resume_texts.keys()), index


resume_texts, resume_names, faiss_index = load_data()

# ---------------- SEARCH ----------------
def search(query_emb, k=20):
    D, I = faiss_index.search(np.array([query_emb], dtype=np.float32), k)

    results = []
    for d, i in zip(D[0], I[0]):
        results.append({
            "resume": resume_names[i],
            "score": float(1 / (1 + d)),
            "text": resume_texts[resume_names[i]]
        })
    return results


# ---------------- JOB DESCRIPTION ----------------
st.markdown("### Job Description")
job_desc = st.text_area("", height=160)

# ---------------- ANALYZE ----------------
if st.button("Analyze Resumes"):

    if not job_desc.strip():
        st.warning("Please enter a job description")
        st.stop()

    query_emb = get_embedding(job_desc)
    results = search(query_emb)

    st.markdown("## Top Matching Candidates")

    shown = 0

    for r in results:
        name, email, phone, skills, experience = extract_candidate_info(r["text"])

        # -------- FILTERS --------
        if r["score"] < min_score:
            continue

        if experience < min_experience:
            continue

        if skill_filter:
            required = [s.strip().lower() for s in skill_filter.split(",")]
            if not any(s in r["text"].lower() for s in required):
                continue

        shown += 1

        with st.expander(f"{shown}. {name} | Score: {r['score']:.2f}"):

            # Candidate Details
            st.markdown(
                f"""
                <div style="background:#f0f8ff;color:#000;padding:14px;border-radius:8px">
                <b>Name:</b> {name}<br>
                <b>Email:</b> {email}<br>
                <b>Phone:</b> {phone}<br>
                <b>Skills:</b> {", ".join(skills) if skills else "Not found"}<br>
                <b>Experience:</b> {experience} years
                </div>
                """,
                unsafe_allow_html=True
            )

            # AI Resume Description (Ollama)
            description = analyze_resume(r["text"][:2000])

            st.markdown(
                f"""
                <div style="background:#ffffff;color:#000;padding:14px;border-radius:8px;margin-top:10px">
                <b>Candidate Description</b><br><br>
                {description}
                </div>
                """,
                unsafe_allow_html=True
            )

    if shown == 0:
        st.warning("No resumes matched the selected filters.")
