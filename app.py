import streamlit as st
import requests
import json

# ১. পেজ সেটআপ ও ডিজাইন (তোমার পছন্দের অরেঞ্জ ট্রান্সপারেন্ট থিম)
st.set_page_config(page_title="Tasnim's AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #000000); }
    .dashboard-container {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(255, 165, 0, 0.1); backdrop-filter: blur(25px);
        padding: 25px 40px; border-radius: 20px;
        border: 1px solid rgba(255, 165, 0, 0.2); margin-bottom: 30px;
    }
    .name-text { color: #ffa500; font-size: 28px; font-weight: 700; text-transform: uppercase; }
    .ai-text { color: #ffffff; font-size: 18px; }
    [data-testid="stChatMessage"] { background: rgba(255, 255, 255, 0.02) !important; border-radius: 15px !important; border: 1px solid rgba(255, 165, 0, 0.1) !important; }
    header, footer {visibility: hidden;}
    </style>
    <div class="dashboard-container">
        <div class="left-sector"><h1 class="name-text">TASNIM AHMED</h1></div>
        <div class="right-sector"><p class="ai-text">AI ASSISTANT</p></div>
    </div>
    """, unsafe_allow_html=True)

# ২. এপিআই কল করার নতুন নিয়ম (Direct Request Method)
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def get_ai_response(user_input):
    payload = {
        "contents": [{"parts": [{"text": user_input}]}]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code}. API এখনো একটিভ হয়নি বা লিমিট শেষ।"

# ৩. চ্যাট ইন্টারফেস
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
