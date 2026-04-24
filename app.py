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
    }
    .main-title { color: #1e3a8a !important; font-size: 30px; font-weight: 700; }
    [data-testid="stChatMessage"] p { color: #111827 !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    <div class="header-container">
        <div class="main-title">🤖 Tasnim's Personal AI</div>
        <p style="color: #374151;">Always active to assist you</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. Gemini AI কনফিগারেশন
# এখানে তোমার সঠিক API Key টি বসানো আছে
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY" 

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Configuration Error: {e}")

# ৪. সেশন স্টেট
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Ami Tasnim-er AI. Aj kivabe sahayyo korte pari?"}]

# ৫. চ্যাট হিস্ট্রি
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f'<p style="color: #111827;">{message["content"]}</p>', unsafe_allow_html=True)

# ৬. ইউজার ইনপুট ও উত্তর
if prompt := st.chat_input("Start a conversation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<p style="color: #111827;">{prompt}</p>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        try:
            # ইনস্ট্রাকশন সেট করা
            response = model.generate_content(f"User is talking to an AI created by Tasnim Ahmed. Answer politely: {prompt}")
            ai_response = response.text
            
            st.markdown(f'<p style="color: #111827;">{ai_response}</p>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            # এখানে আসল সমস্যাটা দেখাবে
            st.error(f"আসল সমস্যাটি হলো: {e}")
