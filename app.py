import streamlit as st
import requests
import json

# ১. পেজ সেটআপ ও প্রফেশনাল ডিজাইন
st.set_page_config(page_title="Tasnim's AI", layout="centered")

st.markdown("""
    <style>
    /* ডার্ক ব্যাকগ্রাউন্ড */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a, #000000);
    }

    /* ট্রান্সপারেন্ট অরেঞ্জ গ্লাস হেডার */
    .header-container {
        text-align: center;
        background: rgba(255, 165, 0, 0.08); /* ট্রান্সপারেন্ট অরেঞ্জ */
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 165, 0, 0.2);
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .name-title {
        color: #ffa500;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .ai-subtitle {
        color: #ffffff;
        font-size: 16px;
        font-weight: 400;
        margin-top: 8px;
        letter-spacing: 1px;
        opacity: 0.8;
    }

    /* চ্যাট বাবল ডিজাইন */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 165, 0, 0.1) !important;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">AI ASSISTANT</div>
        <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 10px;">আমি তাসনিমের তৈরি এআই চ্যাট বট</p>
    </div>
    """, unsafe_allow_html=True)

# ২. সরাসরি এপিআই কানেকশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_ai_response(user_input):
    payload = {"contents": [{"parts": [{"text": user_input}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Please wait a few minutes."
    except:
        return "Connection error. Please try again."

# ৩. চ্যাট সিস্টেম
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("যেকোনো কিছু লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        answer = get_ai_response(prompt)
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
