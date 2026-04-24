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
        <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 10px;">আমি তাসনিমের তৈরি এআই চ্যাট বট</p>
    </div>
    """, unsafe_allow_html=True)

# ২. ফ্রি পাবলিক এপিআই (কোনো Key লাগবে না)
def get_ai_response(text):
    # আমরা একটি ফ্রি পাবলিক চ্যাট এপিআই ব্যবহার করছি
    url = f"https://api.simsimi.vn/v1/simtalk"
    payload = {'text': text, 'lc': 'bn'} # বাংলায় উত্তর দেওয়ার জন্য
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json()['message']
        else:
            return "দুঃখিত, সার্ভার একটু ব্যস্ত। আবার চেষ্টা করুন।"
    except:
        return "ইন্টারনেট কানেকশন চেক করুন।"

# ৩. চ্যাট সিস্টেম
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
        response = get_ai_response(prompt)
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
