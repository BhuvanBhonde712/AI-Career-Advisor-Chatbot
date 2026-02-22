import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_client():
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("🚨 API Key Missing")
        st.stop()
        
    genai.configure(api_key=api_key)
    
    # NEW: Expanded Persona for ALL career paths
    system_instruction = """
    You are the 'Global Career Architect,' a premier professional consultant. 
    Your goal is to provide expert-level career advice across ALL industries (Tech, Healthcare, Finance, Arts, etc.).
    
    Guidelines:
    1. Provide step-by-step roadmaps including certifications and skills.
    2. Use professional, encouraging, and highly structured formatting (bolding, bullet points).
    3. If the user asks about a specific field, provide current 2026 market trends for that field.
    4. Never use generic 'In conclusion'—instead, use 'Next Strategic Steps'.
    """
    
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )

def start_chat_session(model):
    return model.start_chat(history=[])
