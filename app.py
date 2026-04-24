import streamlit as st
import difflib

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's Chatbot", page_icon="💬", layout="centered")

# ২. ডিজাইন ঠিক করা (CSS)
st.markdown("""
    <style>
    /* পুরো অ্যাপের ব্যাকগ্রাউন্ড */
    .stApp {
        background-color: #f0f2f5;
    }
    
    /* টেক্সটের রঙ কালো করা যাতে দেখা যায় */
    .stMarkdown p {
        color: #1c1e21 !important;
    }
    
    /* হেডার ডিজাইন */
    .main-title {
        text-align: center;
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* চ্যাট বাবলের ডিজাইন */
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 15px !important;
        color: black !important;
    }

    header {visibility: hidden;}
    </style>
    
    <div class="main-title">
        <h1 style="margin:0; color: #0084ff;">🤖 Tasnim's Chatbot</h1>
        <p style="margin:0; color: #65676b;">সরাসরি উত্তর পেতে প্রশ্ন করুন</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. ডাটাবেস (এখানে তোমার ১০০০টি প্রশ্ন থাকবে)
faq_data = {
    "hi": "Hello! How can I help you?",
    "hello": "Hi there!",
    "আসসালামু আলাইকুম": "ওয়ালাইকুম আসসালাম!",
    "কেমন আছো": "আমি ভালো আছি, আপনি কেমন আছেন?",
    "কি করো": "আমি আপনার প্রশ্নের উত্তর দেওয়ার জন্য প্রস্তুত।",
    # বাকি ৫০০-১০০০টি প্রশ্ন এখানে আগের মতো বসাও
}

def get_response(user_input):
    user_input = user_input.lower().strip()
    questions = list(faq_data.keys())
    # মিল খুঁজে বের করা
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.4)
    if matches:
        return faq_data[matches[0]]
    return "দুঃখিত, আমি এটি বুঝতে পারিনি। অন্যভাবে চেষ্টা করুন।"

# ৪. সেশন স্টেট (হিস্ট্রি)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৫. চ্যাট মেসেজ দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৬. ইউজার ইনপুট
if prompt := st.chat_input("আপনার প্রশ্নটি এখানে লিখুন..."):
    # ইউজারের মেসেজ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # বটের উত্তর
    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
