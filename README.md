AI Career Assistant (Agentic AI Project)

An end-to-end AI-powered platform that automates job search, generates personalized applications, and provides an interactive interview coaching system with real-time feedback and performance analytics.

✨ Features
💼 Job Assistant
Fetches relevant jobs based on user skills
Avoids duplicate applications using vector similarity (ChromaDB)
Generates personalized cover letters
Tailors resumes for specific roles
🎤 AI Interview Coach
Chatbot-style interview system
Resume-based intelligent questioning
Follow-up technical questions
Voice + text input support
Real-time feedback generation
📊 Performance Analytics
Score tracking per question
Weakness analysis
Performance trends visualization
Downloadable PDF report
🔐 Authentication System
Secure login/register system
Password hashing
User-specific history tracking
🧠 Memory System
Vector database (ChromaDB)
Semantic duplicate job detection
Persistent memory storage
🧠 Tech Stack
Frontend: Streamlit
Backend: Python
LLM: Groq (LLaMA 3.1)
Frameworks: LangChain, LangGraph
Database: SQLite
Vector DB: ChromaDB
ML Libraries: Scikit-learn, Pandas, NumPy
Voice Processing: SpeechRecognition
PDF Generation: ReportLab
🏗️ Architecture

The system follows a multi-agent architecture:

Job Agent → Fetch jobs
Resume Agent → Customize resume
Cover Letter Agent → Generate content
Apply Agent → Simulate application
Interview Agent → Ask questions
Feedback Agent → Evaluate answers

All agents are orchestrated using LangGraph workflow.


<img width="1913" height="860" alt="Screenshot 2026-04-12 212553" src="https://github.com/user-attachments/assets/07a1046d-c302-4721-9e67-9a03ae7a297c" />
<img width="1919" height="884" alt="Screenshot 2026-04-12 213614" src="https://github.com/user-attachments/assets/89eb328a-f8bc-472c-8aa6-a5370cad9e1a" />
<img width="1909" height="923" alt="Screenshot 2026-04-12 213716" src="https://github.com/user-attachments/assets/61bdd798-625e-45ff-b5b1-3057f5983fe0" />
<img width="1919" height="897" alt="Screenshot 2026-04-12 214208" src="https://github.com/user-attachments/assets/bed76b8d-f955-4a9b-8444-eb5b5892b681" />
<img width="1879" height="942" alt="Screenshot 2026-04-12 214242" src="https://github.com/user-attachments/assets/0a23cee6-ea51-49b3-8256-fc12175ae501" />
