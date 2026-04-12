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
    temperature=0.3,
    model_name="llama-3.1-8b-instant"
)

# -----------------------------
# 📊 FEEDBACK AGENT
# -----------------------------
def feedback_agent(answer):

    try:
        prompt = f"""
You are an expert technical interviewer.

Evaluate the following answer:

{answer}

Respond STRICTLY in this format:

Score: <number out of 10>
Strengths: <brief points>
Improvements: <brief points>
"""

        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception as e:
        return f"⚠️ Error generating feedback: {str(e)}"