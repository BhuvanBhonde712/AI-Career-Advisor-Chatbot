# 🚀 AI Career Architect: Intelligent Pathfinding for GenAI & Cloud

An advanced, production-ready AI consultant built with **Gemini 1.5 Flash** and **Streamlit**. This bot acts as a Senior AI Architect and Career Strategist, providing personalized roadmaps, skill-gap analysis, and project-based learning paths for aspiring engineers.

---

## 🌟 Key Features

* **Architect Persona:** Specifically tuned to provide high-level systems design advice alongside career coaching.
* **Skill-Gap Analysis:** Generates targeted learning paths based on current industry trends (MLOps, RAG, LLM Orchestration).
* **Project Roadmapping:** Recommends "Proof-of-Work" projects to help users build a high-value portfolio.
* **Production Architecture:** Built with a modular backend to allow for easy scaling and integration with vector databases.
* **Stateful Memory:** Tracks user background and goals throughout the session for cohesive advice.

## 🏗️ System Architecture

This project follows the **Modular Design Pattern**, separating the UI from the LLM logic to ensure maintainability.

```text
ai-career-advisor/
├── .env                  # Secure API Credentials
├── .gitignore            # Version control safety
├── requirements.txt      # Production dependencies
├── app.py                # Streamlit Frontend (The "Consultation Room")
└── core/                 
    ├── __init__.py       
    ├── prompts.py        # System Instructions (The "Advisor Brain")
    └── gemini_client.py  # Gemini API Orchestration
