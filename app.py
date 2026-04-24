import streamlit as st
import requests
from duckduckgo_search import DDGS

# ১. ডিজাইন (তাসনিম আহমেদ স্পেশাল)
st.set_page_config(page_title="Tasnim's AI", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    .header-container {
        text-align: center;
        background: rgba(255, 165, 0, 0.1); 
        backdrop-filter: blur(20px);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255, 165, 0, 0.3);
        margin-bottom: 35px;
    }
    .name-title { color: #ffa500; font-size: 30px; font-weight: 800; text-transform: uppercase; }
    .ai-subtitle { color: #ffffff; font-size: 14px; opacity: 0.7; }
    </style>
    <div class="header-container">
        <div class="name-title">TASNIM AHMED</div>
        <div class="ai-subtitle">SMART INTERNET AI ASSISTANT</div>
        <p style="color: grey; font-size: 12px;">ইন্টারনেট রিসার্চ ক্ষমতা সম্পন্ন</p>
    </div>
    """, unsafe_allow_html=True)

# ২. ইন্টারনেট সার্চ ফাংশন
def internet_search(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except:
        return ""

# ৩. এআই প্রসেসিং
API_KEY = "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"

def get_ai_response(user_input, history):
    # ইন্টারনেট থেকে তথ্য নিয়ে আসা
    search_data = internet_search(user_input)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    system_prompt = f"""
    তুমি তাসনিম আহমেদের তৈরি একটি স্মার্ট এআই। তোমার কাছে ইন্টারনেট এক্সেস আছে। 
    ইন্টারনেট থেকে পাওয়া লেটেস্ট তথ্য এখানে দেওয়া হলো: {search_data}
    এই তথ্যগুলো ব্যবহার করে ব্যবহারকারীকে সুন্দর বাংলায় উত্তর দাও। 
    যদি ইন্টারনেটে তথ্য না পাও, তবে তোমার নিজের বুদ্ধি ব্যবহার করো।
    """
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "system", "content": system_prompt}] + history,
        "temperature": 0.6
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "ইন্টারনেট রিসার্চ করতে গিয়ে একটু সমস্যা হয়েছে। আবার চেষ্টা করো।"

# ৪. চ্যাট ইন্টারফেস
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("যেকোনো লেটেস্ট তথ্য জানতে চান?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ইন্টারনেটে খুঁজছি..."):
            response = get_ai_response(prompt, st.session_state.chat_history)
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
