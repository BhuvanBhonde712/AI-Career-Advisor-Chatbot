import streamlit as st
import os
from dotenv import load_dotenv
from core.gemini_client import get_gemini_client, start_chat_session

# --- 1. GLOBAL SETTINGS & PROFESSIONAL THEME ---
load_dotenv()
st.set_page_config(
    page_title="Global Career Architect",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a sleek, enterprise-grade feel
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .chat-header { font-size: 2rem; font-weight: bold; color: #1E3A8A; margin-bottom: 0px; }
    .sidebar-text { font-size: 0.9rem; color: #4B5563; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR UTILITIES ---
with st.sidebar:
    st.markdown("### 🛠️ Advisor Console")
    st.markdown("<p class='sidebar-text'>Your strategic partner for 2026 career planning across all industries.</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Feature: Clear Chat
    if st.button("Clear Consultation"):
        st.session_state.messages = []
        st.session_state.chat_session = start_chat_session(st.session_state.model)
        st.rerun()
    
    st.divider()
    st.info("**Instructions:** Provide your current role and your 5-year goal to get a specialized roadmap.")

# --- 3. INITIALIZATION ---
# Using session_state for multi-turn memory as requested
if "model" not in st.session_state:
    with st.spinner("Synchronizing Architect Engine..."):
        st.session_state.model = get_gemini_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = start_chat_session(st.session_state.model)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. MAIN UI LAYOUT ---
st.markdown("<h1 class='chat-header'>💼 Global Career Architect</h1>", unsafe_allow_html=True)
st.caption("Strategic Pathfinding | Market Analysis | Executive Coaching")

# Container for chat messages to keep them organized
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Ex: 'I am a nurse wanting to move into Healthcare Admin' or 'How do I become a Pilot?'"):
    
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response with professional "Analyzing" feedback
    with st.chat_message("assistant"):
        with st.spinner("Drafting your strategic roadmap..."):
            try:
                # Utilizing Gemini 1.5 Flash for the response logic
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"System Error: {str(e)}")
                st.info("Check your API key in the Streamlit Secrets dashboard.")

# --- 6. FOOTER ---
st.markdown("---")
st.markdown("<center><small>Powered by Gemini 1.5 Flash Architecture</small></center>", unsafe_allow_html=True)
