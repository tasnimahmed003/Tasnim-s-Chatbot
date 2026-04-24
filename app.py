import streamlit as st
import difflib

# ১. পেজ টাইটেল এবং হেডার সেটআপ
st.set_page_config(page_title="Tasnim's Chatbot", page_icon="💬")

# CSS দিয়ে মেসেঞ্জারের মতো লুক দেওয়া (ববল ডিজাইন)
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
    }
    header {visibility: hidden;}
    .main-title {
        text-align: center;
        color: #0084ff;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        padding-bottom: 20px;
        border-bottom: 1px solid #ddd;
    }
    </style>
    <h1 class="main-title">Tasnim's Chatbot</h1>
    """, unsafe_allow_html=True)

# ২. FAQ ডাটাবেস (এখানে ৫০০+ প্রশ্ন-উত্তর যোগ করার ফরম্যাট)
# আমি নমুনা দিচ্ছি, আপনি এই একই প্যাটার্নে ৫০০টি পূর্ণ করবেন।
faq_data = {
    # English Version
    "hi": "Hello! How can I help you?",
    "what is your name": "I am Tasnim's AI Chatbot.",
    "how are you": "I'm doing great! What about you?",
    "bye": "Goodbye! Have a nice day.",
    "software engineering": "It involves designing, developing, and maintaining software systems.",
    
    # Bangla Version
    "হাই": "হ্যালো! আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
    "তোমার নাম কি": "আমি তাসনিমের তৈরি একটি চ্যাটবট।",
    "কেমন আছো": "আমি ভালো আছি! আপনার খবর কি?",
    "বিদায়": "ভালো থাকবেন, আবার কথা হবে!",
    "সফটওয়্যার ইঞ্জিনিয়ারিং": "এটি হলো এমন একটি ক্ষেত্র যেখানে সফটওয়্যার তৈরি ও রক্ষণাবেক্ষণ নিয়ে কাজ করা হয়।",
    
    # --- এখানে আপনার বাকি ৫০০টি FAQ যুক্ত করুন ---
}

def get_response(user_input):
    user_input = user_input.lower().strip()
    questions = list(faq_data.keys())
    
    # ইউজার ইনপুট ও ডিকশনারির প্রশ্নের মধ্যে মিল খোঁজা
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.4)
    
    if matches:
        return faq_data[matches[0]]
    else:
        return "I'm sorry, I don't have information on that. / দুঃখিত, এই বিষয়ে আমার কাছে তথ্য নেই।"

# ৩. সেশন স্টেট (মেসেজ হিস্ট্রি রাখার জন্য)
if "messages" not in st.session_state:
    st.session_state.messages = []

# ৪. আগের কনভারসেশন ডিসপ্লে করা
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৫. চ্যাট ইনপুট (মেসেঞ্জারের মতো নিচে থাকবে)
if prompt := st.chat_input("Start a conversation..."):
    # ইউজারের মেসেজ সেভ ও শো করা
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # বটের রেসপন্স জেনারেট করা
    response = get_response(prompt)
    
    # বটের মেসেজ সেভ ও শো করা
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
