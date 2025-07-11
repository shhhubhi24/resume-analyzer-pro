# 🧠 Resume Analyzer Pro — AI-Powered Resume Review Tool

An intelligent, full-stack web application that analyzes resumes, generates scores, and suggests job-specific improvements using AI and rule-based logic.

---

## 🚀 Features

- 📄 **Smart Resume Parsing**: Extracts text and metadata from PDF resumes using `pdfplumber` and `PyPDF2`.
- 🤖 **AI-Powered Feedback**: Integrates **GROQ API (GPT)** via FastAPI to generate real-time, personalized suggestions.
- 🎯 **Scoring Engine**: Evaluates resumes based on keyword matching, job relevance, format quality, and content balance.
- 📊 **ATS & HR-Friendly Suggestions**: Highlights weak sections, suggests improvements for each resume section (summary, experience, skills).
- 🔍 **Job Role-Specific Analysis**: Allows selection of job roles (e.g. Data Analyst, Frontend Developer) for tailored feedback.
- ☁️ **Deployed & Containerized**: Uses Docker for environment control and deployed via **Render (backend)** and **Vercel (frontend)**.

---

## 🛠️ Tech Stack

| Layer        | Tools Used                                           |
|--------------|------------------------------------------------------|
| Frontend     | React.js, Tailwind CSS                              |
| Backend      | FastAPI (Python), REST API                          |
| AI/NLP       | GROQ API (GPT), Rule-Based Logic                    |
| PDF Parsing  | pdfplumber, PyPDF2                                  |
| Database     | PostgreSQL                                          |
| DevOps       | Docker, Render (Backend), Vercel (Frontend), CI/CD |

---

## 🎯 Real-World Use Case

Job seekers often struggle to optimize their resumes for ATS (Applicant Tracking Systems) and HR readability. This tool helps:
- Analyze formatting, keywords, and relevance
- Suggest improvements tailored to job roles
- Increase visibility and clarity of resumes for hiring pipelines

---

## 🌟 Highlight AI Feature

Leverages **GPT via FastAPI** to:
- Rewrite bullet points for impact
- Suggest missing sections based on job role
- Analyze language tone and conciseness
- Recommend skill additions relevant to the field

---

## 💡 Advanced Highlights

- 🧠 Combines **AI + rule-based scoring** for precision and explainability
- 🔍 Uses **text similarity + semantic analysis** for role-relevance scoring
- 🔄 Fully automated **CI/CD deployment with Docker & Render/Vercel**
- 🧪 Tested with a variety of resume formats for robustness

---

## 📷 Screenshots (Optional)
> Include 2–3 screenshots or GIFs showing:
> - Resume upload screen
> - AI-generated suggestions
> - Overall score dashboard

---

## 🧪 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-analyzer-pro.git
cd resume-analyzer-pro

# Backend (Python - FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (React)
cd frontend
npm install
npm start
