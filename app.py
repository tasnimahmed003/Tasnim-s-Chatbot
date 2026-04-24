import streamlit as st
import google.generativeai as genai

# ১. প্রফেশনাল মডার্ন ডিজাইন সেটআপ
st.set_page_config(page_title="Tasnim's Pro AI", layout="centered")

st.markdown("""
    <style>
    /* মডার্ন গ্রেডিয়েন্ট ব্যাকগ্রাউন্ড */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* গ্লাস-মরফিজম হেডার */
    .header-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    .main-title {
        color: white;
        font-size: 35px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0;
    }

    .sub-title {
        color: rgba(255, 255, 255, 0.8);
        font-size: 16px;
        margin-top: 10px;
    }

    /* চ্যাট বাবল ডিজাইন */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-bottom: 10px !important;
    }

    /* টেক্সট কালার সাদা করা */
    .stMarkdown p, p, span {
        color: white !important;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-card">
        <h1 class="main-title">TASNIM AHMED</h1>
        <p class="sub-title">Professional AI Assistant System</p>
    </div>
    """, unsafe_allow_html=True)

# ২. এআই কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # এখানে লেটেস্ট মডেল দেওয়া হয়েছে

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৩. মেসেজ প্রসেসিং
if prompt := st.chat_input("How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # এআই রেসপন্স জেনারেশন
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # এরর হলে সুন্দর করে জানানো
            st.info("API Syncing: আপনার এআই সিস্টেমটি গুগল সার্ভারের সাথে যুক্ত হচ্ছে। দয়া করে ১০ মিনিট পর আবার চেষ্টা করুন।")
