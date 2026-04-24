import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's AI", layout="wide")

# ২. মডার্ন স্প্লিট লেআউট ও অরেঞ্জ ট্রান্সপারেন্ট থিম (CSS)
st.markdown("""
    <style>
    /* ডার্ক ব্যাকগ্রাউন্ডের সাথে অরেঞ্জ গ্লো */
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a, #000000);
    }

    /* ট্রান্সপারেন্ট অরেঞ্জ ড্যাশবোর্ড কন্টেইনার */
    .dashboard-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 165, 0, 0.1); /* হালকা ট্রান্সপারেন্ট অরেঞ্জ */
        backdrop-filter: blur(25px);
        padding: 25px 40px;
        border-radius: 20px;
        border: 1px solid rgba(255, 165, 0, 0.2); /* অরেঞ্জ বর্ডার */
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(255, 165, 0, 0.05);
    }

    .left-sector {
        text-align: left;
        flex: 1;
    }

    .right-sector {
        text-align: right;
        flex: 1;
    }

    /* নাম ছোট এবং প্রফেশনাল */
    .name-text {
        color: #ffa500; /* অরেঞ্জ কালার */
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
        text-transform: uppercase;
    }

    .ai-text {
        color: #ffffff;
        font-size: 18px;
        font-weight: 400;
        margin: 0;
        opacity: 0.9;
    }

    /* চ্যাট ইন্টারফেস */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 165, 0, 0.1) !important;
    }

    .stMarkdown p {
        color: #e0e0e0 !important;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="dashboard-container">
        <div class="left-sector">
            <h1 class="name-text">TASNIM AHMED</h1>
        </div>
        <div class="right-sector">
            <p class="ai-text">AI ASSISTANT</p>
            <p style="color: rgba(255,165,0,0.6); font-size: 13px; margin: 0;">আমি তাসনিমের তৈরি এআই চ্যাট বট</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ৩. এআই কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৪. ইনপুট ও প্রসেসিং
if prompt := st.chat_input("যেকোনো কিছু লিখুন..."):
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
