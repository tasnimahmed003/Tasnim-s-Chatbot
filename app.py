import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Tasnim's AI", layout="centered")

# UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .header-box {
        text-align: center;
        padding: 20px;
        background-color: #161b22;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 25px;
    }
    .main-title { color: #58a6ff; font-family: sans-serif; margin: 0; }
    .developer-info { color: #8b949e; font-size: 14px; margin-top: 5px; }
    [data-testid="stChatMessage"] { background-color: #161b22 !important; border-radius: 10px !important; }
    header, footer { visibility: hidden; }
    </style>
    <div class="header-box">
        <h1 class="main-title">Tasnim Ahmed's AI</h1>
        <p class="developer-info">Professional AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)

# Gemini Configuration
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input and AI Response
if prompt := st.chat_input("Enter your query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            ai_output = response.text
            st.write(ai_output)
            st.session_state.messages.append({"role": "assistant", "content": ai_output})
        except Exception:
            st.error("System is currently syncing with API. Please retry in a few minutes.")
