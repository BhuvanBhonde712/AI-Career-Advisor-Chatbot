import os
import google.generativeai as genai
from dotenv import load_dotenv
from core.prompts import CAREER_ADVISOR_SYSTEM_INSTRUCTION

# Load environment variables
load_dotenv()

# Configure the API Key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_model():
    """
    Initializes the Gemini model with the Career Advisor persona.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", # or "gemini-2.5-flash" based on your local availability
        system_instruction=CAREER_ADVISOR_SYSTEM_INSTRUCTION
    )
    return model

def start_blog_session():
    """
    Starts the multi-turn chat session. 
    (We keep the name 'start_blog_session' so app.py can find it)
    """
    model = get_gemini_model()
    return model.start_chat(history=[])