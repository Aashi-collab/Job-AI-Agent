import streamlit as st
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from workflow.graph import build_graph

# -----------------------------
# 🎨 PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Job Agent",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# 🎨 CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.title {
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    color: #9ca3af;
    margin-bottom: 20px;
}
.success-box {
    background-color: #064e3b;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🧠 SIDEBAR INPUTS
# -----------------------------
with st.sidebar:
    st.header("⚙️ User Profile")

    skills = st.text_input("Skills", "Python, AI")
    role = st.text_input("Target Role", "Data Scientist")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    run_btn = st.button("🚀 Run Agent")

# -----------------------------
# 🏠 MAIN HEADER
# -----------------------------
st.markdown('<div class="title">🤖 AI Job Application Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Automate job search, resume generation & applications</div>', unsafe_allow_html=True)

# -----------------------------
# 📄 RESUME PROCESSING (IMPORTANT)
# -----------------------------
resume_text = ""

if uploaded_file is not None:
    from tools.resume_parser import parse_resume
    resume_text = parse_resume(uploaded_file)

# -----------------------------
# 🚀 RUN AGENT
# -----------------------------
if run_btn:

    with st.spinner("🤖 AI Agent is working..."):

        app = build_graph()

        result = app.invoke({
            "user_profile": {
                "skills": skills.split(","),
                "role": role,
                "resume": resume_text   # ✅ now always defined
            }
        })

    st.markdown('<div class="success-box">✅ Process Completed Successfully</div>', unsafe_allow_html=True)

    st.write("")

    # -----------------------------
    # 📊 OUTPUT SECTION
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Application Result")

        if "feedback" in result:
            st.success(result["feedback"])
        else:
            st.warning("⚠️ Job skipped (already applied or similar found)")

    with col2:
        st.markdown("### 👤 User Info")
        st.write("**Skills:**", skills)
        st.write("**Role:**", role)

if "cover_letter" in result:
    st.markdown("### ✉️ Generated Cover Letter")
    st.write(result["cover_letter"])


# -----------------------------
# 📌 FOOTER
# -----------------------------
st.write("---")
st.caption("Built with ❤️ using AI Agents + LangGraph")