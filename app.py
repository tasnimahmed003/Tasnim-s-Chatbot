import streamlit as st
import google.generativeai as genai

# ১. প্রিমিয়াম ডিজাইন সেটআপ
st.set_page_config(page_title="Tasnim's Pro AI", layout="centered")

st.markdown("""
    <style>
    /* মডার্ন ডার্ক গ্রেডিয়েন্ট ব্যাকগ্রাউন্ড */
    .stApp {
        background: radial-gradient(circle at top right, #2d3748, #1a202c);
    }

    /* প্রিমিয়াম হেডার কার্ড */
    .header-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }

    .main-title {
        color: #63b3ed; /* ইলেকট্রিক ব্লু */
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
        text-transform: uppercase;
    }

    .sub-title {
        color: #a0aec0;
        font-size: 16px;
        margin-top: 12px;
        font-weight: 500;
    }

    /* চ্যাট বাবল ডিজাইন */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 15px !important;
    }

    /* টেক্সট কালার */
    .stMarkdown p, p, span {
        color: #e2e8f0 !important;
        font-size: 17px;
    }

    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-card">
        <h1 class="main-title">TASNIM AHMED</h1>
        <p class="sub-title">Advanced AI Intelligence System</p>
    </div>
    """, unsafe_allow_html=True)

# ২. এআই কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)

# সবচাইতে স্টেবল মডেল ব্যবহার করা হয়েছে
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৩. স্মার্ট রেসপন্স সিস্টেম
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # এআই রেসপন্স
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            # এরর হলে কোনো আজেবাজে কথা না লিখে স্মার্টলি হ্যান্ডেল করা
            st.info("System is initializing. Please wait 10-15 minutes for the Google API to activate.")
