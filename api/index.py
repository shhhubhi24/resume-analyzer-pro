from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.resume_parser import extract_text_from_pdf
from api.job_matcher import match_jobs
from api.gpt_suggester import get_resume_feedback
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import httpx

UPLOAD_DIR = "uploads"
MIN_RESUME_LEN = 100
MAX_FEEDBACK_LEN = 6000

app = FastAPI()
executor = ThreadPoolExecutor()

# CORS (✅ adjust to your deployed frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🔢 Resume Score Logic
def calculate_resume_score(text: str) -> int:
    text_lower = text.lower()
    score = 0

    # 1. ✅ Skills match
    important_skills = ["python", "java", "react", "sql", "machine learning", "data analysis", "docker", "cloud"]
    skill_score = sum(1 for skill in important_skills if skill in text_lower)
    score += min(skill_score * 3, 20)  # max 20

    # 2. 📂 Project mentions
    project_keywords = ["project", "developed", "built", "implemented", "designed"]
    project_score = sum(1 for word in project_keywords if word in text_lower)
    score += min(project_score * 4, 20)  # max 20

    # 3. 📈 Quantifiable results
    if any(char in text for char in ["%", "+", "-", "$", "reduced", "increased", "improved"]):
        score += 15  # bonus for metrics

    # 4. 🧠 Education & Certifications
    if "bachelor" in text_lower or "master" in text_lower or "certification" in text_lower:
        score += 15

    # 5. 📝 Length / completeness
    word_count = len(text.split())
    if 300 <= word_count <= 1000:
        score += 15  # ideal range
    elif word_count > 1000:
        score += 10
    elif word_count < 300:
        score += 5

    return min(score, 100)


# 📥 1. Upload Resume
@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), role: str = Form("General")):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        resume_text = extract_text_from_pdf(file_path).strip()
        if len(resume_text) < MIN_RESUME_LEN:
            raise HTTPException(status_code=400, detail="Resume is too short or unreadable.")

        return {"filename": file.filename, "text": resume_text}

    except Exception as e:
        print("❌ Resume upload error:", e)
        raise HTTPException(status_code=500, detail="Internal error during resume processing.")

# 🤖 2. Suggest Improvements (Groq)
@app.post("/suggest-improvements/")
async def suggest_improvements(payload: dict):
    resume_text = payload.get("resume_text", "")
    role = payload.get("role", "General")

    if len(resume_text.strip()) < MIN_RESUME_LEN:
        raise HTTPException(status_code=400, detail="Resume is too short for feedback.")
    if len(resume_text) > MAX_FEEDBACK_LEN:
        raise HTTPException(status_code=400, detail="Resume is too long for feedback.")

    try:
        feedback = await asyncio.get_event_loop().run_in_executor(
            executor, get_resume_feedback, resume_text, role
        )
        if not feedback or "No valid content" in feedback:
            raise HTTPException(status_code=500, detail="AI feedback model returned no suggestions.")

        return feedback

    except Exception as e:
        print("❌ GPT feedback error:", e)
        raise HTTPException(status_code=500, detail="Internal error while generating feedback.")

# 📊 3. Score Resume
@app.post("/score-resume/")
async def score_resume(payload: dict):
    resume_text = payload.get("resume_text", "")
    if not resume_text:
        raise HTTPException(status_code=400, detail="Missing resume text.")
    return {"score": calculate_resume_score(resume_text)}

# 🎯 4. Match Jobs
@app.post("/match-jobs/")
async def match_jobs_route(payload: dict):
    resume_text = payload.get("resume_text", "")
    if not resume_text:
        raise HTTPException(status_code=400, detail="Missing resume text.")
    matches = match_jobs(resume_text)  # ✅ not async anymore
    return {"matches": matches}

# ✅ Groq API Check Endpoint
@app.get("/test-groq/")
async def test_groq():
    try:
        response = await httpx.get("https://api.groq.com/")  # ✅ FIXED
        return {"status": response.status_code, "text": response.text}
    except Exception as e:
        return {"error": str(e)}
