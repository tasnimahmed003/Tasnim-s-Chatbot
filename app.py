import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's AI", layout="centered")

# ২. আল্ট্রা-মডার্ন ট্রান্সপারেন্ট গ্লাস ডিজাইন
st.markdown("""
    <style>
    /* ডার্ক গ্রেডিয়েন্ট ব্যাকগ্রাউন্ড */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e);
    }

    /* ট্রান্সপারেন্ট গ্লাস হেডার */
    .header-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 40px;
    }

    .main-title {
        color: #ffffff;
        font-size: 30px;
        font-weight: 700;
        margin: 0;
    }

    .sub-title {
        color: rgba(255, 255, 255, 0.7);
        font-size: 16px;
        margin-top: 10px;
    }

    /* চ্যাট বাবল ডিজাইন */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    .stMarkdown p {
        color: #e0e0e0 !important;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-card">
        <h1 class="main-title">TASNIM AHMED</h1>
        <p class="sub-title">আমি তাসনিমের তৈরি এআই চ্যাট বট</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. এআই সেটআপ
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৪. ইনপুট ও রেসপন্স
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.info("Please wait a few minutes.")
