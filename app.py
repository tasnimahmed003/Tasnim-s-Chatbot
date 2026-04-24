import streamlit as st
import requests
import json

# ১. পেজ সেটআপ ও প্রফেশনাল ডিজাইন
st.set_page_config(page_title="Tasnim's AI", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a, #000000);
    }

    /* ট্রান্সপারেন্ট অরেঞ্জ গ্লাস হেডার */
    .header-container {
        text-align: center;
        background: rgba(255, 165, 0, 0.08);
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 165, 0, 0.2);
        margin-bottom: 35px;
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
        margin-top: 8px;
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

# ২. Groq API কানেকশন (পৃথিবীর দ্রুততম এআই)
GROQ_API_KEY = "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"
URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(user_input):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant created by Tasnim Ahmed."},
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}. API কী-তে সমস্যা হতে পারে।"
    except:
        return "Connection error."

# ৩. চ্যাট সিস্টেম
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("যেকোনো কিছু জিজ্ঞেস করুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        answer = get_groq_response(prompt)
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
