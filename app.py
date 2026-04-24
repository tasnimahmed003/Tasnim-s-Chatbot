import streamlit as st
import difflib

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's Chatbot", page_icon="💬", layout="centered")

# ২. প্রফেশনাল মডার্ন ডিজাইন (CSS)
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড */
    .stApp {
        background-color: #f0f2f5;
    }
    
    /* হেডার ডিজাইন */
    .main-title {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1c1e21;
        padding: 20px;
        background: white;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }

    /* চ্যাট বাবলের ডিজাইন */
    .stChatMessage {
        background-color: white !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
        margin-bottom: 15px !important;
    }

    /* ইনপুট বক্সের স্টাইল */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }

    /* সাইডবার বা অপ্রয়োজনীয় মেনু হাইড করা */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div class="main-title">
        <h1 style="margin:0; font-size: 24px;">🤖 Tasnim's Chatbot</h1>
        <p style="margin:0; color: #65676b; font-size: 14px;">Always active to help you</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. ডাটাবেস (এখানে তোমার আগের সব FAQ থাকবে)
faq_data = {
    "hi": "Hello! How can I help you?",
    "আসসালামু আলাইকুম": "ওয়ালাইকুম আসসালাম! আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
    "কেমন আছো": "আমি ভালো আছি! আপনি কেমন আছেন?",
    # ... তোমার বাকি সব ১০০০টি প্রশ্ন এখানে বসাও ...
}

def get_response(user_input):
    user_input = user_input.lower().strip()
    questions = list(faq_data.keys())
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.4)
    return faq_data[matches[0]] if matches else "Sorry, I don't know the answer. / দুঃখিত, আমি উত্তরটি জানি না।"

# ৪. সেশন স্টেট (মেসেজ হিস্ট্রি)
if "messages" not in st.session_state:
    # শুরুতে একটি ওয়েলকাম মেসেজ থাকবে যাতে স্ক্রিন ফাঁকা না লাগে
    st.session_state.messages = [
        {"role": "assistant", "content": "হ্যালো! আমি তাসনিমের চ্যাটবট। আপনাকে কীভাবে সাহায্য করতে পারি?"}
    ]

# ৫. চ্যাট মেসেজ ডিসপ্লে
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৬. চ্যাট ইনপুট
if prompt := st.chat_input("আপনার প্রশ্নটি এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
