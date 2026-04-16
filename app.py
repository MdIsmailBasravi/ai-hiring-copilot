import streamlit as st
from PyPDF2 import PdfReader
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# MODELS
# =========================
model = SentenceTransformer('all-MiniLM-L6-v2')
rag_model = SentenceTransformer('all-MiniLM-L6-v2')

# =========================
# PDF TEXT EXTRACTION
# =========================
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# =========================
# SKILLS
# =========================
SKILLS = [
    "python", "java", "sql", "flask", "django",
    "api", "machine learning", "pandas", "numpy"
]

def extract_skills(text):
    text = text.lower()
    return list(set([s for s in SKILLS if s in text]))

# =========================
# ML SCORE
# =========================
def semantic_score(resume, job):
    r = model.encode([resume])
    j = model.encode([job])
    return round(cosine_similarity(r, j)[0][0] * 100, 2)

# =========================
# RAG (MULTI-CHUNK IMPROVED)
# =========================
def chunk_text(text):
    return [c.strip() for c in text.split(". ") if len(c) > 20]

def get_top_chunks(question, resume_text, top_k=3):
    chunks = chunk_text(resume_text)

    if len(chunks) == 0:
        return "No relevant data found."

    chunk_embeddings = rag_model.encode(chunks)
    question_embedding = rag_model.encode([question])

    scores = np.dot(chunk_embeddings, question_embedding.T).flatten()

    top_indices = scores.argsort()[-top_k:][::-1]

    results = []
    for i in top_indices:
        results.append(f"• {chunks[i]}")

    return "\n".join(results)

# =========================
# DECISION ENGINE
# =========================
def decision(score):
    if score >= 75:
        return "🟢 Strong Candidate"
    elif score >= 50:
        return "🟡 Medium Candidate"
    else:
        return "🔴 Weak Candidate"

def eligibility(score, missing):
    if score >= 75 and len(missing) <= 2:
        return "Highly Eligible ✅"
    elif score >= 50:
        return "Partially Eligible ⚠️"
    else:
        return "Not Eligible ❌"

def confidence(score):
    return f"{min(100, max(0, score)):.0f}% Confidence"

# =========================
# UI DESIGN
# =========================
st.set_page_config(page_title="AI Hiring Copilot", layout="wide")

st.title("🚀 AI Hiring Copilot PRO")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)")
job_desc = st.text_area("💼 Paste Job Description")

resume_text = ""

# =========================
# PROCESS
# =========================
if uploaded_file:
    resume_text = extract_text(uploaded_file)

if resume_text and job_desc:

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = semantic_score(resume_text, job_desc)

    # =========================
    # DASHBOARD UI
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Match Score", f"{score}%")

    with col2:
        st.metric("Matched Skills", len(matched))

    with col3:
        st.metric("Missing Skills", len(missing))

    st.progress(int(score))

    # =========================
    # RESULTS
    # =========================
    st.subheader("🧠 Decision")
    st.success(decision(score))

    st.subheader("🎯 Eligibility")
    st.info(eligibility(score, missing))

    st.subheader("📊 Confidence")
    st.write(confidence(score))

    # =========================
    # SKILLS
    # =========================
    st.subheader("✔ Matched Skills")
    st.write(matched)

    st.subheader("❌ Missing Skills")
    st.write(missing)

    # =========================
    # RAG SECTION
    # =========================
    st.subheader("💬 Ask Resume (AI Insight)")
    question = st.text_input("Ask anything about resume")

    if question:
        st.write("🔍 Top Relevant Resume Parts:")
        st.write(get_top_chunks(question, resume_text))

# =========================
# RESUME DISPLAY
# =========================
if uploaded_file:
    st.subheader("📄 Resume Preview")
    st.write(resume_text)
