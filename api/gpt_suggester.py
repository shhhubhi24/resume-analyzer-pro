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

        prompt = f"""
        You are an expert resume reviewer.

        Review the following resume text for the role of {role}.

        Return:
        1. **3 specific suggestions for improvement**, formatted as bullet points.
        2. **Skills/tools missing** — also in bullet points.
        3. **Formatting/tone improvements** — again, in bullet points.
        4. Keep the response under 500 words. Use **Markdown** for styling.

        Resume:
        \"\"\"
        {resume_text}
        \"\"\"
        """

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
