import streamlit as st
import json
import os
from core.gemini_client import start_blog_session

# 1. Database Logic: Local JSON Storage
USER_DB = "users.json"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    with open(USER_DB, "w") as f:
        json.dump(users, f)
    return True

# 2. Page Configuration
st.set_page_config(page_title="CareerArchitect Pro", page_icon="💼", layout="wide")

# 3. Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# --- AUTHENTICATION INTERFACE ---
def auth_page():
    st.container()
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.title("👨‍💼 CareerArchitect Pro")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.subheader("Login")
            u_login = st.text_input("Username", key="l_user")
            p_login = st.text_input("Password", type="password", key="l_pass")
            if st.button("Login", use_container_width=True):
                users = load_users()
                if u_login in users and users[u_login] == p_login:
                    st.session_state.authenticated = True
                    st.session_state.chat_session = start_blog_session()
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            st.subheader("Create Account")
            u_signup = st.text_input("New Username", key="s_user")
            p_signup = st.text_input("New Password", type="password", key="s_pass")
            if st.button("Register", use_container_width=True):
                if u_signup and p_signup:
                    if save_user(u_signup, p_signup):
                        st.success("Account created! Please switch to Login tab.")
                    else:
                        st.error("Username already exists.")
                else:
                    st.warning("Please fill in both fields.")

# --- MAIN APP LOGIC ---
if not st.session_state.authenticated:
    auth_page()
else:
    # --- Sidebar: Profile & Logout ---
    with st.sidebar:
        st.title("👤 Dashboard")
        st.write("Career Mode: **Active**")
        st.divider()
        exp_level = st.select_slider("Experience", ["Student", "Junior", "Mid", "Senior"])
        target_role = st.text_input("Target Role", value="AI Engineer")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- Chat Interface ---
    st.title("🚀 Career Strategy Workspace")
    
    # Display Chat
    chat_box = st.container(height=450)
    with chat_box:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    # Input Logic
    if prompt := st.chat_input("Ask your advisor..."):
        with chat_box:
            st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Injecting Context
        full_prompt = f"CONTEXT: [Level: {exp_level}, Role: {target_role}] REQUEST: {prompt}"

        with chat_box:
            with st.chat_message("assistant"):
                with st.status("Analyzing...", expanded=False):
                    response = st.session_state.chat_session.send_message(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})