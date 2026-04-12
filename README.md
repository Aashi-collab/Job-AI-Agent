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