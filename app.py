import streamlit as st
import requests

# ১. প্রিমিয়াম অরেঞ্জ গ্লাস ডিজাইন
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
    .name-title { color: #ff8800; font-size: 28px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .ai-subtitle { color: #ffffff; font-size: 16px; opacity: 0.8; margin-top: 5px; }
    .made-by { color: rgba(255, 255, 255, 0.6); font-size: 13px; margin-top: 10px; font-style: italic; }
    
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
    }
    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">AI ASSISTANT</div>
        <div class="made-by">আমি তাসনিমের তৈরি এআই অ্যাসিস্ট্যান্ট</div>
    </div>
    """, unsafe_allow_html=True)

# ২. এআই পার্সোনালিটি সেটআপ
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system", 
                "content": """তোমার নাম 'Tasnim's AI'। তুমি তাসনিম আহমেদের তৈরি একজন বুদ্ধিমান অ্যাসিস্ট্যান্ট। 
                তোমার ব্যবহারের নিয়মাবলী:
                ১. কথা শুরু করার সময় সবসময় 'আসসালামু আলাইকুম' বলবে। কখনোই 'নমস্কার' বা অন্য কিছু বলবে না।
                ২. নিজেকে সবসময় 'আমি তাসনিম আহমেদের তৈরি এআই অ্যাসিস্ট্যান্ট' হিসেবে পরিচয় দেবে। 
                ৩. ব্যবহারকারী যেই হোক না কেন, তাকে সম্মান দিয়ে মানুষের মতো সাবলীল বাংলায় কথা বলবে।
                ৪. অতিরিক্ত রোবটিক কথাবার্তা এড়িয়ে চলবে এবং টু-দ্য-পয়েন্ট উত্তর দেবে।"""
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "দুঃখিত, আমি এই মুহূর্তে কানেক্ট হতে পারছি না।"
    except:
        return "ইন্টারনেট কানেকশন চেক করুন।"

# ৩. চ্যাট ইন্টারফেস
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("বার্তা লিখুন..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        res = get_ai_response(prompt)
        st.write(res)
        st.session_state.chat_history.append({"role": "assistant", "content": res})
