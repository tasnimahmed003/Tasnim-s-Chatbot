import streamlit as st
import requests

# ১. প্রিমিয়াম ডিজাইন (অরেঞ্জ ট্রান্সপারেন্ট গ্লাস)
st.set_page_config(page_title="Tasnim's AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #1a1a1a, #0b0b0b); }
    .header-container {
        text-align: center;
        background: rgba(255, 136, 0, 0.1); 
        backdrop-filter: blur(25px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 136, 0, 0.3);
        margin-bottom: 35px;
    }
    .name-title { color: #ff8800; font-size: 28px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .ai-subtitle { color: #ffffff; font-size: 16px; opacity: 0.8; margin-top: 5px; }
    .made-by { color: rgba(255, 255, 255, 0.6); font-size: 13px; margin-top: 10px; font-style: italic; }
    
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
    }
    header, footer {visibility: hidden;}
    </style>
    
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">AI ASSISTANT</div>
        <div class="made-by">আমি তাসনিমের তৈরি এআই অ্যাসিস্ট্যান্ট</div>
    </div>
    """, unsafe_allow_html=True)

# ২. Groq API কানেকশন
API_KEY = "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"

def get_ai_response(history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # এআই-কে স্মার্ট করার জন্য মূল নির্দেশনা (System Prompt)
    system_message = {
        "role": "system", 
        "content": "You are a highly intelligent AI assistant created by Tasnim Ahmed. Speak in natural, fluent Bengali. Do not repeat yourself. Answer questions accurately based on facts. Be friendly but professional. If you don't know something, admit it politely."
    }
    
    # মেমোরি এবং সিস্টেম মেসেজ একসাথে পাঠানো
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [system_message] + history,
        "temperature": 0.6, # একুরেসি বাড়ানোর জন্য কমানো হয়েছে
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "দুঃখিত, আমি এখন উত্তর দিতে পারছি না। একটু পরে চেষ্টা করো।"
    except:
        return "ইন্টারনেট কানেকশন চেক করো।"

# ৩. চ্যাট ইন্টারফেস এবং স্মৃতি
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# আগের মেসেজগুলো দেখানো
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("যেকোনো প্রশ্ন করুন..."):
    # ইউজারের মেসেজ যোগ করা
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # আগের সব কথা মনে রেখে উত্তর দেওয়া
        response = get_ai_response(st.session_state.chat_history)
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
