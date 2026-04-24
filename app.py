import streamlit as st
import requests

# ১. প্রফেশনাল অরেঞ্জ গ্লাস ডিজাইন
st.set_page_config(page_title="Tasnim's AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #0b0b0b); }
    .header-container {
        text-align: center;
        background: rgba(255, 136, 0, 0.1); 
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 136, 0, 0.3);
        margin-bottom: 35px;
    }
    .name-title { color: #ff8800; font-size: 28px; font-weight: 800; letter-spacing: 2px; margin: 0; }
    .ai-subtitle { color: #ffffff; font-size: 16px; margin-top: 5px; opacity: 0.8; }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 136, 0, 0.1) !important;
    }
    header, footer {visibility: hidden;}
    </style>
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">AI ASSISTANT</div>
    </div>
    """, unsafe_allow_html=True)

# ২. Groq API - সরাসরি কানেকশন
API_KEY = "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"

def get_response(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": text}]
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            # এররটা সরাসরি দেখার জন্য
            return f"Error: {res.status_code}. API কী বা কানেকশনে সমস্যা।"
    except Exception as e:
        return f"Error: {str(e)}"

# ৩. চ্যাট ইন্টারফেস
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("এআইকে কিছু লিখুন..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = get_response(prompt)
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
