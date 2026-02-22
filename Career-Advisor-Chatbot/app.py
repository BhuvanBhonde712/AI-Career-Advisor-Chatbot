import streamlit as st
import os
from dotenv import load_dotenv
from core.gemini_client import get_gemini_client, start_chat_session

# --- 1. CONFIGURATION & STYLING ---
load_dotenv()
st.set_page_config(page_title="Global Career Architect", page_icon="💼", layout="wide")

# Professional CSS for Login and Chat
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .login-box {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: auto;
    }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1E3A8A; color: white; font-weight: bold; }
    .chat-header { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("Secure Access")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Replace 'admin' and 'password123' with your preferred credentials
        # In production, these should be stored in st.secrets
        if username == "admin" and password == "password123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. THE CHATBOT INTERFACE (RENDERED AFTER LOGIN) ---
def main_app():
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### 🛠️ Advisor Console")
        st.info("Logged in as: **Admin**")
        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_session = start_chat_session(st.session_state.model)
            st.rerun()

    # --- INITIALIZE CORE ENGINE ---
    if "model" not in st.session_state:
        st.session_state.model = get_gemini_client()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = start_chat_session(st.session_state.model)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- CHAT UI ---
    st.markdown("<h1 class='chat-header'>💼 Global Career Architect</h1>", unsafe_allow_html=True)
    st.caption("Strategic Pathfinding | Market Analysis | Multi-Industry Coaching")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ex: 'Plan a transition from Sales to Data Science'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting 2026 market data..."):
                # Using Gemini 1.5 Flash for career logic
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 4. EXECUTION FLOW ---
if not st.session_state.logged_in:
    login()
else:
    main_app()
