import streamlit as st
from PyPDF2 import PdfReader
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

# =========================
# DB IMPORT
# =========================
from db import init_db, add_user, check_user, save_result, get_history

# =========================
# INIT
# =========================
init_db()
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Hiring Copilot PRO", layout="wide")
st.title("🚀 AI Hiring Copilot PRO (SaaS Version)")

# =========================
# SESSION STATE FIX
# =========================
if "user" not in st.session_state:
    st.session_state["user"] = None

# =========================
# SIDEBAR LOGIN SYSTEM (FIXED)
# =========================
st.sidebar.title("🔐 Account System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if menu == "Register":
    if st.sidebar.button("Register"):
        if username and password:
            add_user(username, password)
            st.success("User created ✔ Please login")
        else:
            st.error("Enter username & password")

elif menu == "Login":
    if st.sidebar.button("Login"):
        user = check_user(username, password)
        if user:
            st.session_state["user"] = username
            st.success("Login successful ✔")
            st.rerun()   # 🔥 IMPORTANT FIX
        else:
            st.error("Invalid credentials ❌")

# =========================
# BLOCK IF NOT LOGGED IN
# =========================
if not st.session_state["user"]:
    st.warning("Please login to continue 🚀")
    st.stop()

st.success(f"Welcome {st.session_state['user']} 👋")

# =========================
# PDF EXTRACTION
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
# AI SCORE
# =========================
def semantic_score(resume, job):
    r = model.encode([resume])
    j = model.encode([job])
    return round(cosine_similarity(r, j)[0][0] * 100, 2)

# =========================
# GPT FUNCTION
# =========================
def ask_gpt(resume_text, job_desc, question):

    prompt = f"""
You are an AI Hiring Assistant.

Resume:
{resume_text}

Job Description:
{job_desc}

User Question:
{question}

Give clear answer with:
- Eligibility
- Skill gaps
- Explanation
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# INPUT UI
# =========================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)")
job_desc = st.text_area("💼 Job Description")

resume_text = ""

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.subheader("📄 Resume Preview")
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

    # SAVE TO DB
    save_result(st.session_state["user"], score, matched, missing)

    # DASHBOARD
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("AI Score", f"{score}%")

    with col2:
        st.metric("Matched Skills", len(matched))

    with col3:
        st.metric("Missing Skills", len(missing))

    st.progress(int(score))

    st.subheader("🧠 Skills Analysis")
    st.write("✔ Matched:", matched)
    st.write("❌ Missing:", missing)

# =========================
# GPT CHAT
# =========================
st.subheader("💬 AI Assistant")

question = st.text_input("Ask something")

if question and resume_text and job_desc:
    with st.spinner("Thinking..."):
        answer = ask_gpt(resume_text, job_desc, question)
        st.write(answer)

# =========================
# HISTORY
# =========================
st.subheader("📊 Your History")

history = get_history(st.session_state["user"])

for h in history:
    st.write("Score:", h[0])
    st.write("Matched:", h[1])
    st.write("Missing:", h[2])
    st.write("---")
