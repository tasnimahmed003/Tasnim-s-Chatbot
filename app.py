import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's AI Assistant", page_icon="🤖", layout="centered")

# ২. ডিজাইন (CSS)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .header-container {
        text-align: center; background: rgba(255, 255, 255, 0.9);
        padding: 20px; border-radius: 20px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-title { color: #1e3a8a !important; font-size: 30px; font-weight: 700; margin: 0; }
    
    /* মেসেজ টেক্সট কালার ফিক্স */
    [data-testid="stChatMessage"] p, .stMarkdown p { 
        color: #000000 !important; 
        font-weight: 500;
        line-height: 1.6;
    }
    
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        border: 1px solid #d1d5db !important;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    <div class="header-container">
        <div class="main-title">🤖 Tasnim's Personal AI</div>
        <p style="color: #374151; font-weight: bold;">Developed by Tasnim Ahmed</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. Gemini AI কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY" 

try:
    genai.configure(api_key=API_KEY)
    # এখানে মডেলের নাম পরিবর্তন করে gemini-pro দেওয়া হয়েছে যা সবখানে কাজ করে
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Config Error: {e}")

# ৪. সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Ami Tasnim-er AI. Aj kivabe sahayyo korte pari?"}]

# ৫. চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৬. ইউজার ইনপুট ও এআই রেসপন্স
if prompt := st.chat_input("যেকোনো কিছু লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # এআই দিয়ে উত্তর তৈরি
            response = model.generate_content(f"You are a helpful AI created by Tasnim Ahmed. Answer this: {prompt}")
            ai_response = response.text
            
            st.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error(f"এখনো সমস্যা হচ্ছে? আসল কারণ: {e}")
