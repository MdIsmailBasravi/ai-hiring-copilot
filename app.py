import streamlit as st
from PyPDF2 import PdfReader

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# AI MODELS
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
# SKILL SYSTEM
# =========================
SKILLS = [
    "python", "java", "sql", "flask", "django",
    "api", "machine learning", "pandas", "numpy"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return list(set(found))

# =========================
# SEMANTIC SCORE (ML)
# =========================
def semantic_score(resume, job):
    r = model.encode([resume])
    j = model.encode([job])

    score = cosine_similarity(r, j)[0][0]
    return round(score * 100, 2)

# =========================
# RAG SYSTEM
# =========================
def chunk_text(text):
    return text.split(". ")

def get_relevant_chunks(question, resume_text):
    chunks = chunk_text(resume_text)

    chunk_embeddings = rag_model.encode(chunks)
    question_embedding = rag_model.encode([question])

    scores = np.dot(chunk_embeddings, question_embedding.T)

    top_index = np.argmax(scores)
    best_chunk = chunks[top_index]

    return f"""
🔍 Relevant Resume Info:
{best_chunk}

💡 Interpretation:
This part of resume is most relevant to: "{question}"
"""

# =========================
# DECISION ENGINE
# =========================
def explain_decision(score):
    if score > 70:
        return "Strong candidate — good match with job requirements."
    elif score > 40:
        return "Average candidate — some skills missing."
    else:
        return "Weak candidate — major skill gaps."

def resume_tips(missing):
    if len(missing) == 0:
        return "Good resume. Add more real-world projects to stand out."
    return "Improve these skills: " + ", ".join(missing)

# =========================
# UI
# =========================
st.title("AI Hiring Copilot v2 🚀")

uploaded_file = st.file_uploader("Upload Resume (PDF)")
job_desc = st.text_area("Paste Job Description")

resume_text = ""

# =========================
# PROCESS RESUME
# =========================
if uploaded_file:
    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Text")
    st.write(resume_text)

# =========================
# ANALYSIS
# =========================
if resume_text and job_desc:

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = semantic_score(resume_text, job_desc)

    st.subheader("🧠 Skill Analysis")
    st.write("✔ Matched Skills:", matched)
    st.write("❌ Missing Skills:", missing)

    st.subheader("📊 AI Match Score")
    st.write(score, "%")

    st.subheader("🧠 Hiring Decision")
    st.write(explain_decision(score))

    st.subheader("📌 Improvement Tips")
    st.write(resume_tips(missing))

# =========================
# RAG CHAT
# =========================
st.subheader("💬 Ask About Resume")

question = st.text_input("Ask something (e.g. Am I good for ML role?)")

if question and resume_text:
    answer = get_relevant_chunks(question, resume_text)
    st.write(answer)
