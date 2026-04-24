import streamlit as st
import difflib

# ১. পেজ সেটআপ
st.set_page_config(page_title="Tasnim's Chatbot", page_icon="💬", layout="centered")

# ২. ডিজাইন ঠিক করা (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f5;
    }
    .stMarkdown p {
        color: #1c1e21 !important;
    }
    .main-title {
        text-align: center;
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 15px !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div class="main-title">
        <h1 style="margin:0; color: #0084ff;">🤖 Tasnim's Chatbot</h1>
        <p style="margin:0; color: #65676b;">সরাসরি উত্তর পেতে প্রশ্ন করুন</p>
    </div>
    """, unsafe_allow_html=True)

# ৩. ডাটাবেস
faq_data = {
    # --- সাধারণ আড্ডা (বাংলা) ---
    "কেমন আছো": "আমি খুব ভালো আছি! আপনি কেমন আছেন?",
    "কেমন আছেন": "জি ভালো, ধন্যবাদ। আপনার দিনকাল কেমন যাচ্ছে?",
    "কি খবর": "এই তো চলছে, আপনার খবর কি বলুন?",
    "কি করো": "আমি আপনার সাথে কথা বলছি এবং আপনার প্রশ্নের উত্তর দেওয়ার চেষ্টা করছি।",
    "কি করছো": "এই তো আপনার মেসেজের জন্য বসে আছি!",
    "ভাত খেয়েছ": "আমি তো রোবট, আমার ক্ষুধা লাগে না। তবে জিজ্ঞেস করার জন্য অনেক ধন্যবাদ!",
    "খাওয়া দাওয়া করেছো": "জি না, আমি শুধু ডেটা আর বিদ্যুৎ খেয়ে বেঁচে থাকি!",
    "বাসার সবাই কেমন আছে": "আশা করি আপনার পরিবারের সবাই খুব ভালো আছেন।",
    "তোমার নাম কি": "আমার নাম তাসনিম'স চ্যাটবট।",
    "তুমি কি বন্ধু হবে": "অবশ্যই! আমি আপনার ভার্চুয়াল বন্ধু।",
    "বিয়ে করেছ": "না, আমার বিয়ে করার সুযোগ নেই!",
    "আজকের দিনটা কেমন": "খুবই চমৎকার! আপনি যদি ইতিবাচক থাকেন তবে দিনটি দারুণ কাটবে।",
    "মন খারাপ": "মন খারাপ করবেন না। একটু গান শুনুন বা বাইরের তাজা বাতাসে ঘুরে আসুন।",
    "ধন্যবাদ": "আপনাকেও অসংখ্য ধন্যবাদ আমার সাথে কথা বলার জন্য।",
    "ভালোবাসা কি": "ভালোবাসা হলো একে অপরের প্রতি শ্রদ্ধা এবং টান।",
    
    # --- Greetings & Casual (English/Banglish) ---
    "hi": "Hello! How can I help you?",
    "hello": "Hi there! What's on your mind?",
    "assalamualaikum": "Walaikum Assalam! How are you?",
    "আসসালামু আলাইকুম": "ওয়ালাইকুম আসসালাম! আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
    "ki khobor": "Sob bhaloi, apni kemon achen?",
    "kemon acho": "Ami bhalo achi, apni?",
    "what are you doing": "I am processing your requests.",
    "ami bored": "Cholen kotha boli! Tech ba programming niye kisu jigges koren.",
    "tumar nam ki": "Amar nam Tasnim's Chatbot.",

    # --- Technology & General ---
    "what is python": "Python is a high-level, interpreted programming language.",
    "python ki": "Python holo ekta khub e popular programming language.",
    "পাইথন কি": "পাইথন একটি শক্তিশালী এবং সহজ প্রোগ্রামিং ভাষা।",
    "cpu ki": "CPU holo computer er brain.",
    "hardware ki": "Computer er vouto ongso gulo holo hardware.",
    "software ki": "Software holo kichu instructions er somosthi.",
    "সূর্য কোন দিকে ওঠে": "সূর্য পূর্ব দিকে ওঠে।",
    "national fruit of bd": "Jackfruit is the national fruit of Bangladesh.",
    "funny joke": "Why was the computer cold? Because it left its Windows open!",
    "koutuk": "শিক্ষক: বল্টু বল তো মশা কয় প্রকার? বল্টু: স্যার, মশা ৫ প্রকার। কামড়ানো মশা, না কামড়ানো মশা, প্যানপ্যানানি মশা, উড়ন্ত মশা আর মশারী ভেদ করা মশা!"
}

def get_response(user_input):
    user_input = user_input.lower().strip()
    questions = list(faq_data.keys())
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.4)
    if matches:
        return faq_data[matches[0]]
    return "দুঃখিত, আমি এটি বুঝতে পারিনি। অন্যভাবে চেষ্টা করুন।"

# ৪. সেশন স্টেট (হিস্ট্রি)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "হ্যালো! আমি তাসনিমের চ্যাটবট। আপনাকে কীভাবে সাহায্য করতে পারি?"}]

# ৫. চ্যাট মেসেজ দেখানো
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ৬. ইউজার ইনপুট
if prompt := st.chat_input("আপনার প্রশ্নটি এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
