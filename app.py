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

# ২. Groq API কানেকশন (Fixing the 400 Error)
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    # Payload ফরম্যাট আপডেট করা হয়েছে
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            # সরাসরি এরর ডিটেইলস দেখাবে যাতে আমরা বুঝতে পারি
            error_details = response.json().get('error', {}).get('message', 'Unknown Error')
            return f"Error {response.status_code}: {error_details}"
    except Exception as e:
        return f"Connection error: {str(e)}"

# ৩. চ্যাট সিস্টেম
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("যেকোনো কিছু জিজ্ঞেস করো..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = get_ai_response(prompt)
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
