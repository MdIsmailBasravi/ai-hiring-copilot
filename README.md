# 🚀 AI Hiring Copilot PRO

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![AI](https://img.shields.io/badge/AI-NLP-green)
![Status](https://img.shields.io/badge/Status-Live-success)

---

## 🌐 Live Demo

👉https://ai-hiring-copilot-uekhnkujd3ynprnkrj6hzs.streamlit.app/

---

## 📌 Overview

AI Hiring Copilot PRO is a **smart resume analyzer** that compares resumes with job descriptions using **AI + NLP**.

It helps:

* Job seekers improve resumes
* Recruiters quickly evaluate candidates

---

## ✨ Features

* 🔐 Secure Login & Registration
* 📄 Resume Upload (PDF)
* 🧠 AI Matching Score
* 🛠 Skill Gap Analysis
* 💬 AI Chat Assistant
* 📊 User History Tracking

---

## 🧠 How It Works

```id="1q6i0z"
Resume → Text Extraction → Embedding → Similarity Score → AI Analysis
```

* Uses **Sentence Transformers** for semantic similarity
* Uses **OpenAI API** for intelligent responses

---

## 🖥️ Screenshots

### 📊 Dashboard

![Dashboard](<img width="1920" height="1020" alt="Screenshot 2026-04-17 153046" src="https://github.com/user-attachments/assets/f19fc8b4-9095-44b1-bb8a-581692de6a5a" />
)


### 💬 AI Assistant

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** SQLite
* **ML Model:** all-MiniLM-L6-v2
* **AI API:** OpenAI

---

## 📂 Project Structure

```id="g73hlr"
ai-hiring-copilot/
│
├── app.py
├── db.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone Repo

```bash id="sbc8ko"
git clone https://github.com/your-username/ai-hiring-copilot.git
cd ai-hiring-copilot
```

### 2. Install Dependencies

```bash id="1l6l9n"
pip install -r requirements.txt
```

### 3. Add API Key

```id="9bp3d7"
OPENAI_API_KEY=your_api_key_here
```

### 4. Run App

```bash id="gjqf5c"
streamlit run app.py
```

---

## 📈 Example Output

| Metric         | Value        |
| -------------- | ------------ |
| AI Score       | 78%          |
| Matched Skills | Python, SQL  |
| Missing Skills | Django, APIs |

---

## ⚠️ Current Limitations

* Basic skill extraction
* No password encryption
* SQLite not scalable

---

## 🔮 Future Scope

* 🔐 Secure authentication (bcrypt)
* 💳 Payment integration (Stripe)
* 📄 Export reports (PDF)
* ☁️ Cloud database (PostgreSQL)

---

## 👨‍💻 Author

**Ismail Basravi**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
