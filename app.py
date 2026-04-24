import streamlit as st
import google.generativeai as genai

# ১. পেজ সেটআপ এবং আইকন
st.set_page_config(page_title="Tasnim's Professional AI", page_icon="🤖", layout="centered")

# ২. প্রফেশনাল এবং মডার্ন "Glassmorphism" ডিজাইন (Custom CSS)
st.markdown("""
    <style>
    /* পুরো পেজের ব্যাকগ্রাউন্ড - একটি হালকা নীল ও বেগুনি গ্রেডিয়েন্ট */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* উপরের হেডার বক্স */
    .header-box {
        text-align: center;
        padding: 30px;
        background: rgba(255, 255, 255, 0.5); /* স্বচ্ছ সাদা */
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 25px;
    }
    .main-title {
        color: #1e40af; /* গাঢ় নীল */
        font-family: 'Poppins', sans-serif;
        font-size: 30px;
        font-weight: 700;
        margin: 0;
    }
    .developer-info {
        color: #4b5563; /* গ্রে */
        font-size: 15px;
        margin-top: 5px;
    }

    /* চ্যাট মেসেজের সাধারণ স্টাইল */
    [data-testid="stChatMessage"] {
        padding: 15px !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }

    /* ইউজারের মেসেজের স্টাইল - একটু স্বচ্ছ সাদা */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #111827 !important;
    }
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    /* এআই/অ্যাসিস্ট্যান্টের মেসেজের স্টাইল - স্বচ্ছ নীল */
    [data-testid="stChatMessageAssistant"] {
        background: rgba(219, 234, 254, 0.7) !important; /* হালকা নীল */
        border: 1px solid rgba(191, 219, 254, 0.4) !important;
    }

    /* ডিফল্ট Streamlit এলিমেন্ট লুকাতে */
    header, footer { visibility: hidden; }
    </style>
    
    <div class="header-box">
        <h1 class="main-title">Tasnim Ahmed's AI</h1>
        <p class="developer-info">A Professional AI Assistant | Developed by Tasnim Ahmed</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. Gemini AI কনফিগারেশন
API_KEY = "AIzaSyAwYbi_pX1NlKarAZi-NopGdKgqf6EIvIY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# ৪. চ্যাট হিস্ট্রি
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৫. চ্যাট হিস্ট্রি দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৬. ইউজার ইনপুট ও উত্তর তৈরি
if prompt := st.chat_input("Enter your query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # বটকে একটি প্রফেশনাল পার্সোনালিটি ইনস্ট্রাকশন দাও
            instruction = "You are a professional and polite AI assistant created by Tasnim Ahmed. Respond naturally in the language the user uses."
            full_prompt = f"{instruction}\nUser: {prompt}"
            
            response = model.generate_content(full_prompt)
            ai_output = response.text
            
            st.write(ai_output)
            st.session_state.messages.append({"role": "assistant", "content": ai_output})
        except Exception:
            # যদি এখনো এপিআই চালু না হয়, তবে এই এরর দেখাবে
            st.error("Model access issue. Please try again in 5 minutes.")
