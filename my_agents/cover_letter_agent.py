from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# -----------------------------
# 🔐 LOAD ENV
# -----------------------------
load_dotenv()

# -----------------------------
# 🤖 LLM INIT
# -----------------------------
llm = ChatGroq(
    temperature=0.4,
    model_name="llama-3.1-8b-instant"
)

# -----------------------------
# ✉️ COVER LETTER AGENT
# -----------------------------
def cover_letter_agent(job, user_profile):

    resume = user_profile.get("resume", "")
    skills = user_profile.get("skills", [])

    try:
        prompt = f"""
You are a professional career assistant.

Write a strong, personalized cover letter.

Job Title: {job['title']}
Company: {job['company']}

Candidate Skills: {skills}

Resume:
{resume[:1000]}

Requirements:
- Professional tone
- Personalized content
- 150–200 words
- Highlight relevant skills
"""

        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception as e:
        return f"⚠️ Error generating cover letter: {str(e)}"

