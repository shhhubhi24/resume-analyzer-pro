import os
import textwrap
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("❌ GROQ_API_KEY not loaded from .env")

print("🔧 Checking GROQ_API_KEY:", api_key[:6], "...")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",  # ✅ Important!
)

def get_resume_feedback(resume_text: str, role: str = "General") -> str:
    try:
        print("📤 Sending resume to Groq (LLaMA3) with role:", role)

        prompt = textwrap.dedent(f"""
        You are an expert career advisor. Analyze the following resume for a candidate applying as a {role}.

        Provide:
        1. Three specific suggestions to improve the resume.
        2. Skills/tools that are missing for a {role}.
        3. Formatting or tone improvements.

        Resume:
        {resume_text}
        """)

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful and expert resume reviewer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Error in get_resume_feedback() with Groq:", e)
        return "❌ An error occurred while generating feedback. Please try again."
