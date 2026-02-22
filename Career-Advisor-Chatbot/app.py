import streamlit as st
import os
from dotenv import load_dotenv
from core.gemini_client import get_gemini_client, start_chat_session

# --- 1. SETTINGS & STYLING ---
load_dotenv()
st.set_page_config(page_title="Career Architect Pro", page_icon="💼", layout="centered")

st.markdown("""
    <style>
    .auth-container {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
    }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE INITIALIZATION ---
# Simulated database for users
if "user_db" not in st.session_state:
    st.session_state.user_db = {} # Format: {"username": "password"}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# --- 3. AUTHENTICATION FUNCTIONS ---
def toggle_auth():
    if st.session_state.auth_mode == "login":
        st.session_state.auth_mode = "signup"
    else:
        st.session_state.auth_mode = "login"

def sign_up_ui():
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.subheader("📝 Create Architect Account")
    new_user = st.text_input("Choose Username", key="reg_user")
    new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
    
    if st.button("Register"):
        if not new_user or not new_pass:
            st.error("Fields cannot be empty.")
        elif new_user in st.session_state.user_db:
            st.error("Username already exists.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            st.session_state.user_db[new_user] = new_pass
            st.success("Account created! Please Sign In.")
            st.session_state.auth_mode = "login"
            st.rerun()
            
    st.write("Already have an account?")
    st.button("Back to Sign In", on_click=toggle_auth)
    st.markdown("</div>", unsafe_allow_html=True)

def sign_in_ui():
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.subheader("🔐 Sign In")
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Access Advisor"):
        if user in st.session_state.user_db and st.session_state.user_db[user] == pw:
            st.session_state.authenticated = True
            st.session_state.current_user = user
            st.rerun()
        else:
            st.error("Invalid username or password. (Did you Sign Up first?)")
            
    st.write("New here?")
    st.button("Create an Account", on_click=toggle_auth)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. MAIN APPLICATION INTERFACE ---
def main_chatbot():
    # Sidebar for logout and utilities
    with st.sidebar:
        st.title("💼 Architect Pro")
        st.write(f"Active User: **{st.session_state.current_user}**")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
        st.divider()
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.session_state.chat_session = start_chat_session(st.session_state.model)
            st.rerun()

    # Chat Engine Initialization
    if "model" not in st.session_state:
        st.session_state.model = get_gemini_client()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = start_chat_session(st.session_state.model)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("Global Career Architect")
    st.caption("Strategic Pathfinding for any Profession")

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input using Gemini 1.5 Flash logic
    if prompt := st.chat_input("Where do you want to take your career?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting Architect Engine..."):
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 5. ROUTING ---
if not st.session_state.authenticated:
    if st.session_state.auth_mode == "login":
        sign_in_ui()
    else:
        sign_up_ui()
else:
    main_chatbot()
