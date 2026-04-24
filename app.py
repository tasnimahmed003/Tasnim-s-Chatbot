import streamlit as st
import requests

# ১. ডিজাইন (অরেঞ্জ ট্রান্সপারেন্ট গ্লাস)
st.set_page_config(page_title="Tasnim's AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #0b0b0b); }
    .header-container {
        text-align: center;
        background: rgba(255, 136, 0, 0.1); 
        backdrop-filter: blur(20px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 136, 0, 0.3);
        margin-bottom: 35px;
    }
    .name-title { color: #ff8800; font-size: 28px; font-weight: 800; text-transform: uppercase; }
    .ai-subtitle { color: #ffffff; font-size: 16px; opacity: 0.8; }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
    }
    header, footer {visibility: hidden;}
    </style>
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">AI ASSISTANT</div>
    </div>
    """, unsafe_allow_html=True)

# ২. লেটেস্ট মডেল আপডেট (llama-3.1-8b-instant)
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",  # নতুন মডেল
        "messages": [{"role": "user", "content": user_input}]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: মডেল বা এপিআই-তে সমস্যা।"
    except:
        return "Connection Error."

# ৩. চ্যাট হিস্ট্রি
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        res = get_ai_response(prompt)
        st.write(res)
        st.session_state.chat_history.append({"role": "assistant", "content": res})
