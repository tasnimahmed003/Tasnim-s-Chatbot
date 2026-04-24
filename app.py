import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's AI Assistant", page_icon="🤖", layout="centered")

# ২. প্রফেশনাল ও মডার্ন ডিজাইন (Custom CSS)
st.markdown("""
    <style>
    /* পুরো ব্যাকগ্রাউন্ড */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* হেডার সেকশন */
    .header-container {
        text-align: center;
        background: rgba(255, 255, 255, 0.8);
        padding: 30px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 30px;
    }

    .main-title {
        color: #1e3a8a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #4b5563;
        font-size: 16px;
        font-style: italic;
    }

    /* চ্যাট বাবল স্টাইল */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        border: 1px solid #e5e7eb !important;
    }

    /* ইনপুট বক্সের ডিজাইন */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div class="header-container">
        <div class="main-title">🤖 Tasnim's Personal AI</div>
        <div class="sub-title">Developed by Tasnim Ahmed | Always active to assist you</div>
    </div>
    """, unsafe_allow_html=True)

# ৩. Gemini AI কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ৪. সেশন স্টেট (চ্যাট হিস্ট্রি)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ami Tasnim-er toiri AI assistant. Aj apnake kivabe sahayyo korte pari?"}
    ]

# ৫. চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৬. ইউজার ইনপুট ও রেসপন্স
if prompt := st.chat_input("Start a conversation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # বটকে প্রফেশনাল পার্সোনালিটি দেওয়া
            instruction = "You are a professional and polite AI assistant created by Tasnim Ahmed. Your responses should be intelligent, helpful, and natural. Use the same language as the user."
            full_prompt = f"{instruction}\nUser: {prompt}"
            
            response = model.generate_content(full_prompt)
            ai_response = response.text
            
            st.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error("Connection issue! Please check your internet or requirements.txt file.")
