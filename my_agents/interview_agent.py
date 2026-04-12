from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# -----------------------------
# 🔐 LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# 🤖 INITIALIZE LLM
# -----------------------------
llm = ChatGroq(
    temperature=0.5,
    model_name="llama-3.1-8b-instant"
)

# -----------------------------
# 🎤 INTERVIEW AGENT
# -----------------------------
def interview_agent(user_profile, previous_answer=None):

    role = user_profile.get("role", "Data Scientist")
    skills = user_profile.get("skills", [])
    resume = user_profile.get("resume", "")

    try:
        # -----------------------------
        # 🟢 FIRST QUESTION
        # -----------------------------
        if previous_answer is None:
            prompt = f"""
You are a professional technical interviewer.

Role: {role}
Skills: {skills}

Candidate Resume:
{resume[:1000]}

Ask the FIRST interview question.

Guidelines:
- Relevant to role and skills
- Use resume if available
- Keep it clear and professional
"""

        # -----------------------------
        # 🔁 FOLLOW-UP QUESTION
        # -----------------------------
        else:
            prompt = f"""
You are a professional technical interviewer.

Candidate's previous answer:
{previous_answer}

Ask a FOLLOW-UP question:
- Go deeper into concepts
- Test practical understanding
- Keep it concise
"""

        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception as e:
        return f"⚠️ Error generating question: {str(e)}"