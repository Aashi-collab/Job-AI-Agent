import streamlit as st
import sys
import os
import speech_recognition as sr
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from workflow.graph import build_graph
from my_agents.interview_agent import interview_agent
from my_agents.feedback_agent import feedback_agent
from utils.score_parser import extract_score
from utils.report_generator import generate_report
from utils.analysis import analyze_weakness
from database.auth import login, register
from database.history import save_history, get_history
from tools.resume_parser import parse_resume

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Assistant", layout="wide")

# -----------------------------
# 🎨 PREMIUM UI
# -----------------------------
st.markdown("""
<style>
body {background-color: #f5f7fb;}
.main {background-color: #f5f7fb;}
h1, h2, h3 {color: #1f2937;}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIN
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None

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
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Register"):
            if register(username, password):
                st.success("Registered!")
            else:
                st.error("Username exists")

    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🤖 AI Career Assistant")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "💼 Job Assistant", "🎤 Interview Coach", "📊 History"]
)

# -----------------------------
# 🏠 HOME
# -----------------------------
if page == "🏠 Home":
    st.title("🚀 AI Career Assistant")
    st.write("Prepare smarter. Get hired faster.")

    st.image(
        "https://images.unsplash.com/photo-1677442136019-21780ecad995",
        use_container_width=True
    )

# -----------------------------
# 💼 JOB AGENT
# -----------------------------
elif page == "💼 Job Assistant":

    st.title("💼 Job Assistant")

    st.image(
        "https://images.unsplash.com/photo-1559028012-481c04fa702d",
        use_container_width=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    skills = st.text_input("Skills", "Python, AI")
    role = st.text_input("Role", "Data Scientist")

    file = st.file_uploader("Upload Resume", type=["pdf"])
    resume_text = parse_resume(file) if file else ""

    if st.button("🚀 Run Agent"):

        with st.spinner("Running AI Agent..."):
            app = build_graph()

            result = app.invoke({
                "user_profile": {
                    "skills": skills.split(","),
                    "role": role,
                    "resume": resume_text
                }
            })

        if "feedback" in result:
            st.success(result["feedback"])

        if "cover_letter" in result:
            st.markdown("### ✉️ Cover Letter")
            st.write(result["cover_letter"])

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🎤 INTERVIEW COACH
# -----------------------------
elif page == "🎤 Interview Coach":

    st.title("🎤 AI Interview Coach")

    st.image(
        "https://images.unsplash.com/photo-1607746882042-944635dfe10e",
        use_container_width=True
    )

    # SESSION
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "scores" not in st.session_state:
        st.session_state.scores = []
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []
    if "started" not in st.session_state:
        st.session_state.started = False

    role = st.text_input("Role", "Data Scientist")
    skills = st.text_input("Skills", "Python, ML")

    resume_file = st.file_uploader("Upload Resume (for deep interview)", type=["pdf"])
    resume_text = parse_resume(resume_file) if resume_file else ""

    if st.button("Start Interview"):
        st.session_state.messages = []
        st.session_state.scores = []
        st.session_state.feedbacks = []
        st.session_state.started = True

        q = interview_agent({
            "role": role,
            "skills": skills.split(","),
            "resume": resume_text
        })

        st.session_state.messages.append({"role": "ai", "content": q})

    # CHAT DISPLAY
    for msg in st.session_state.messages:
        if msg["role"] == "ai":
            st.chat_message("assistant").write(msg["content"])
        else:
            st.chat_message("user").write(msg["content"])

    # VOICE INPUT
    audio_file = st.file_uploader("🎤 Upload Voice", type=["wav"])
    user_input = None

    if audio_file:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(audio_file.read())
            path = f.name

        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)

        try:
            user_input = recognizer.recognize_google(audio)
            st.success(user_input)
        except:
            st.error("Voice not recognized")

    # TEXT INPUT
    text_input = st.chat_input("Your answer...")
    if text_input:
        user_input = text_input

    if user_input and st.session_state.started:

        if user_input.lower() in ["exit", "quit"]:
            st.chat_message("assistant").write("👋 Interview ended")
            st.session_state.started = False
            st.stop()

        st.session_state.messages.append({"role": "user", "content": user_input})

        fb = feedback_agent(user_input)
        score = extract_score(fb)

        st.session_state.scores.append(score)
        st.session_state.feedbacks.append(fb)

        save_history(st.session_state.user, score, fb)

        st.session_state.messages.append({
            "role": "ai",
            "content": f"📊 Feedback:\n{fb}"
        })

        next_q = interview_agent({
            "role": role,
            "skills": skills.split(","),
            "resume": resume_text
        }, user_input)

        st.session_state.messages.append({"role": "ai", "content": next_q})

        st.rerun()

    # ANALYTICS
    if st.session_state.scores:

        st.markdown("### 📊 Performance Dashboard")

        avg = sum(st.session_state.scores) / len(st.session_state.scores)

        st.metric("Average Score", f"{avg:.2f}/10")
        st.line_chart(st.session_state.scores)

        st.markdown("### 🧠 Weakness Analysis")
        st.info(analyze_weakness(st.session_state.scores))

        if st.button("📄 Download Report"):
            file = generate_report(
                st.session_state.scores,
                st.session_state.feedbacks,
                st.session_state.user
            )

            with open(file, "rb") as f:
                st.download_button("Download PDF", f)

# -----------------------------
# HISTORY
# -----------------------------
elif page == "📊 History":

    st.title("📊 Interview History")

    data = get_history(st.session_state.user)

    if not data:
        st.info("No history yet")

    for d in data:
        st.markdown(f"### ⭐ Score: {d[0]}")
        st.write(d[1])
        st.caption(d[2])
        st.write("---")