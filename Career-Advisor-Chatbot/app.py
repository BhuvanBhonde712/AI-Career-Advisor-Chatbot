import streamlit as st
import os
from dotenv import load_dotenv
# Ensure your gemini_client.py is inside a folder named 'core'
from core.gemini_client import get_gemini_client, start_chat_session

# 1. Page Configuration
st.set_page_config(
    page_title="AI Career Architect",
    page_icon="🚀",
    layout="centered"
)

# 2. Header Section
st.title("🚀 AI Career Architect")
st.markdown("""
Welcome to your 2026 Career Strategy Suite. 
I specialize in **Cloud Computing, AI, and Machine Learning** pathfinding.
""")
st.divider()

# 3. Initialize the AI Engine & Session State
# This ensures we don't restart the AI model every time the user types a message
if "model" not in st.session_state:
    with st.spinner("Initializing Architect Brain..."):
        st.session_state.model = get_gemini_client()

if "chat_session" not in st.session_state:
    # This starts the native Gemini multi-turn memory
    st.session_state.chat_session = start_chat_session(st.session_state.model)

if "messages" not in st.session_state:
    # This stores the chat history to display in the UI
    st.session_state.messages = []

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input and Response Logic
if prompt := st.chat_input("Ask about your AI career path (e.g., 'How do I learn MLOps?')"):
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display Assistant response
    with st.chat_message("assistant"):
        try:
            # We send the message to the session so the bot remembers context
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
            st.markdown(full_response)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Tip: Check your Streamlit Secrets and API quota.")

# 6. Sidebar for Project Info
with st.sidebar:
    st.header("Project Info")
    st.info("Built with Gemini 1.5 Flash & Streamlit")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat_session = start_chat_session(st.session_state.model)
        st.rerun()
