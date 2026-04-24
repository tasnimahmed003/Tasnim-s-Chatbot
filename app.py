import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's AI", layout="wide")

# ২. আল্ট্রা-মডার্ন স্প্লিট লেআউট (CSS)
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1e293b, #0f172a);
    }

    /* নাম এবং অ্যাসিস্ট্যান্ট সেকশনকে আলাদা করার জন্য কন্টেইনার */
    .dashboard-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
    }

    .left-sector {
        text-align: left;
        flex: 1;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .right-sector {
        text-align: right;
        flex: 1;
        padding-left: 20px;
    }

    .name-text {
        color: #ffffff;
        font-size: 45px;
        font-weight: 900;
        letter-spacing: 5px;
        margin: 0;
        text-transform: uppercase;
    }

    .ai-text {
        color: #63b3ed;
        font-size: 22px;
        font-weight: 500;
        margin: 0;
    }

    /* চ্যাট ইন্টারফেস */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="dashboard-container">
        <div class="left-sector">
            <h1 class="name-text">TASNIM AHMED</h1>
        </div>
        <div class="right-sector">
            <p class="ai-text">MY AI ASSISTANT</p>
            <p style="color: rgba(255,255,255,0.5); font-size: 14px; margin: 0;">আমি তাসনিমের তৈরি এআই চ্যাট বট</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ৩. এআই কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# চ্যাট ডিসপ্লে
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
