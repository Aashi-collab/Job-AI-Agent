import streamlit as st
import sys
import os
import speech_recognition as sr
import tempfile
from database.auth import login, register
from database.history import save_history, get_history

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_agents.interview_agent import interview_agent
from my_agents.feedback_agent import feedback_agent
from utils.score_parser import extract_score
from utils.report_generator import generate_report
from utils.analysis import analyze_weakness

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    with sr.AudioFile(temp_audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return "Could not understand audio"

# -----------------------------
# 🎨 PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Interview", layout="wide")

st.title("🎤 AI Mock Interview")
st.write("Practice interviews with AI")


# -----------------------------
# 🧠 SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

if "scores" not in st.session_state:
    st.session_state.scores = []

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

if "user" not in st.session_state:
    st.session_state.user = None  
# -----------------------------
# 📥 INPUT FIELDS
# -----------------------------
role = st.text_input("Role", "Data Scientist")
skills = st.text_input("Skills", "Python, ML")

# -----------------------------
# 🚀 START INTERVIEW
# -----------------------------
if st.button("Start Interview"):
    st.session_state.scores = []
    st.session_state.started = True
    st.session_state.messages = []  # reset chat

    first_q = interview_agent({
        "role": role,
        "skills": skills.split(",")
    })

    st.session_state.messages.append({
        "role": "ai",
        "content": first_q
    })


if st.session_state.user is None:

    st.title("🔐 Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = username
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Register"):
            register(username, password)
            st.success("Registered successfully")

    st.stop()
# -----------------------------
# 💬 CHAT DISPLAY
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "ai":
        st.chat_message("assistant").write(msg["content"])
    else:
        st.chat_message("user").write(msg["content"])


if st.session_state.scores:

    st.markdown("### 📊 Performance Tracker")

    avg_score = sum(st.session_state.scores) / len(st.session_state.scores)
    
    st.markdown("### 🧠 Weakness Analysis")

    weakness = analyze_weakness(st.session_state.scores)
    st.info(weakness)

    st.metric("⭐ Average Score", f"{avg_score:.2f}/10")
    st.metric("📌 Questions Answered", len(st.session_state.scores))

    st.line_chart(st.session_state.scores)

    st.markdown("### 🎤 Or upload voice answer")

    audio_file = st.file_uploader("Upload audio (wav)", type=["wav"])

if st.session_state.scores:

    if st.button("📄 Download Report"):

        file = generate_report(
            st.session_state.scores,
            st.session_state.feedbacks
        )

        with open(file, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="interview_report.pdf"
            )
# -----------------------------
# ✍️ USER INPUT
# -----------------------------
if st.session_state.started:
    user_input = st.chat_input("Your answer...")

    # 🎤 Handle voice input
if audio_file is not None:
    user_input = speech_to_text(audio_file)
    st.success(f"Recognized: {user_input}")

    if user_input:

        # 🔥 EXIT FEATURE
        if user_input.lower() in ["exit", "quit", "stop"]:
            st.session_state.messages.append({
                "role": "ai",
                "content": "👋 Interview ended. Great job!"
            })
            st.session_state.started = False
            st.rerun()

        # Save user answer
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # -----------------------------
        # 📊 FEEDBACK
        # -----------------------------
        fb = feedback_agent(user_input)
        st.session_state.feedbacks.append(fb)

        score = extract_score(fb)

        save_history(
        st.session_state.user,
        score,
        fb
)

        score = extract_score(fb)
        st.session_state.scores.append(score)

        st.session_state.messages.append({
            "role": "ai",
            "content": f"📊 Feedback:\n{fb}"
        })

        # -----------------------------
        # 🎤 NEXT QUESTION
        # -----------------------------
        next_q = interview_agent({
            "role": role,
            "skills": skills.split(",")
        }, user_input)

        st.session_state.messages.append({
            "role": "ai",
            "content": next_q
        })

        st.rerun()

        st.markdown("### 📜 Interview History")

history = get_history(st.session_state.user)

for h in history:
    st.write(f"⭐ Score: {h[0]} | 🕒 {h[2]}")
    st.write(h[1])
    st.write("---")