"""
Streamlit UI for AI Resume Screener (HR-facing).
"""

# ------------------------------------------------------------
# Fix import path (IMPORTANT)
# ------------------------------------------------------------
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
import streamlit as st
from core.vector_store import get_resumes_collection, search_resumes
from core.rag_engine import rag_reasoning
from core.ranker import rank_candidates


# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screener for HR Teams")

# ------------------------------------------------------------
# Load persistent collection
# ------------------------------------------------------------
collection = get_resumes_collection()

# ------------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------------
st.sidebar.header("Settings")

top_k = st.sidebar.slider("Top results", 1, 20, 5)
use_rag = st.sidebar.checkbox("Enable AI Explanation", True)

# ----------- FILTERS ----------------
st.sidebar.subheader("Filters")

skill_text = st.sidebar.text_input(
    "Required Skills (comma separated)",
    placeholder="python, aws, docker"
)

# Convert text → list
skill_filter = [
    s.strip().lower()
    for s in skill_text.split(",")
    if s.strip()
]

exp_filter = st.sidebar.slider(
    "Minimum Experience (Years)",
    0, 15, 2
)

# ------------------------------------------------------------
# Main input
# ------------------------------------------------------------
job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Looking for a Python developer with ML and NLP experience..."
)

# ------------------------------------------------------------
# Search
# ------------------------------------------------------------
if st.button("Search Resumes"):

    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        with st.spinner("Searching resumes..."):

            results = search_resumes(
                job_description,
                top_k,
                skills=skill_filter,
                min_exp=exp_filter
            )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        if not documents:
            st.error("No resumes found. Try adjusting filters.")
        else:
            # -------- RANKING SYSTEM --------
            resume_data = []
            for doc, meta in zip(documents, metadatas):
                resume_data.append({
                    "text": doc,
                    "metadata": meta
                })

            ranked_resumes = rank_candidates(
                skill_filter,
                exp_filter,
                resume_data
            )

            st.success(f"Found {len(ranked_resumes)} ranked resumes")

            # -------- DISPLAY --------
            for i, res in enumerate(ranked_resumes, 1):

                doc = res["text"]
                meta = res["metadata"]
                score = res["score"]

                if not doc or not isinstance(doc, str):
                    st.warning("⚠️ Empty resume chunk skipped.")
                    continue

                st.markdown(f"### 📄 Rank #{i} | Score: {score}%")
                st.write(f"**File:** `{meta.get('filename', 'Unknown')}`")

                with st.expander("View Resume Chunk"):
                    st.write(doc)

                if use_rag:
                    with st.spinner("Generating explanation..."):
                        explanation = rag_reasoning(
                            doc,
                            "Explain how well this resume matches the job description."
                        )

                    st.markdown("**AI Explanation:**")
                    st.write(explanation)

                st.divider()
