import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load local .env if it exists (for local testing)
load_dotenv()

def get_gemini_client():
    # Priority 1: Streamlit Cloud Secrets | Priority 2: Local .env
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("🚨 API Key Missing: Please add 'GOOGLE_API_KEY' to your Streamlit Secrets.")
        st.stop()
        
    genai.configure(api_key=api_key)
    
    # Define the strict Persona
    system_instruction = """
    You are a Lead AI Career Architect. Your goal is to guide users in 2026 
    through Cloud Computing, AI, and Machine Learning career paths. 
    Be professional, technical, and encouraging. 
    Always suggest specific tools like AWS, Kubernetes, or Gemini API.
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )
    return model

def start_chat_session(model):
    # Initialize native Gemini chat with memory
    return model.start_chat(history=[])

