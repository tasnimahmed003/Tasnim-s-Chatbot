import streamlit as st
import requests

# ১. প্রিমিয়াম ডিজাইন (অরেঞ্জ ট্রান্সপারেন্ট গ্লাস)
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

# ২. Groq API কানেকশন উইথ মেমোরি
API_KEY = "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"

def get_ai_response(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "দুঃখিত, একটু পরে আবার চেষ্টা করো।"
    except:
        return "ইন্টারনেট কানেকশন চেক করো।"

# ৩. চ্যাট সিস্টেম এবং মেমোরি ম্যানেজমেন্ট
if "messages" not in st.session_state:
    # শুরুতে এআই-কে তার পরিচয় এবং স্বভাব বুঝিয়ে দেওয়া হলো
    st.session_state.messages = [
        {"role": "system", "content": "তুমি তাসনিম আহমেদের তৈরি এআই। তোমার নাম তাসনিম'স এআই। মানুষের মতো স্বাভাবিকভাবে কথা বলো। প্রতিবার উত্তরের শুরুতে নিজের পরিচয় দেওয়ার দরকার নেই। একবার সালাম দিলে পরেরবার সরাসরি উত্তর দিবে। বন্ধুর মতো কথা বলো।"}
    ]

# চ্যাট হিস্ট্রি ডিসপ্লে (ইউজার এবং অ্যাসিস্ট্যান্টের মেসেজগুলো দেখাবে)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("কথা বলুন..."):
    # ইউজারের মেসেজ মেমোরিতে যোগ করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # পুরো মেমোরি (History) এআই-কে পাঠানো হচ্ছে
        res = get_ai_response(st.session_state.messages)
        st.write(res)
        # এআই-এর উত্তর মেমোরিতে যোগ করা
        st.session_state.messages.append({"role": "assistant", "content": res})
