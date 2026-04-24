import streamlit as st
import requests
import json

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's AI", layout="centered")

# ২. প্রিমিয়াম অরেঞ্জ ট্রান্সপারেন্ট গ্লাস ডিজাইন
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a, #000000);
    }

    /* গ্লাস হেডার কন্টেইনার */
    .header-container {
        text-align: center;
        background: rgba(255, 165, 0, 0.08); /* অরেঞ্জ ট্রান্সপারেন্সি */
        backdrop-filter: blur(25px);
        padding: 35px;
        border-radius: 24px;
        border: 1px solid rgba(255, 165, 0, 0.2);
        margin-bottom: 40px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }

    .name-title {
        color: #ffa500;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .ai-subtitle {
        color: #ffffff;
        font-size: 16px;
        font-weight: 400;
        margin-top: 10px;
        opacity: 0.8;
    }

    /* চ্যাট বাবল ডিজাইন */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 165, 0, 0.1) !important;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">AI ASSISTANT</div>
    </div>
    """, unsafe_allow_html=True)

# ৩. Groq API কানেকশন
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
            {"role": "system", "content": "You are a helpful AI assistant created by Tasnim Ahmed. Answer clearly and professionally."},
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "Please wait a few minutes."
    except:
        return "Connection error. Please try again."

# ৪. চ্যাট ইন্টারফেস
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
