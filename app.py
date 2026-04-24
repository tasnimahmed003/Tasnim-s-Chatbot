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
        # --- Greetings & Casual (English, Bangla, Banglish) ---
    # --- সাধারণ আড্ডা (বাংলা) ---
        "কেমন আছো": "আমি খুব ভালো আছি! আপনি কেমন আছেন?",
        "কেমন আছেন": "জি ভালো, ধন্যবাদ। আপনার দিনকাল কেমন যাচ্ছে?",
        "কি খবর": "এই তো চলছে, আপনার খবর কি বলুন?",
        "কি করো": "আমি আপনার সাথে কথা বলছি এবং আপনার প্রশ্নের উত্তর দেওয়ার চেষ্টা করছি।",
        "কি করছো": "এই তো আপনার মেসেজের জন্য বসে আছি!",
        "ভাত খেয়েছ": "আমি তো রোবট, আমার ক্ষুধা লাগে না। তবে জিজ্ঞেস করার জন্য অনেক ধন্যবাদ!",
        "খাওয়া দাওয়া করেছো": "জি না, আমি শুধু ডেটা আর বিদ্যুৎ খেয়ে বেঁচে থাকি!",
        "বাসার সবাই কেমন আছে": "আশা করি আপনার পরিবারের সবাই খুব ভালো আছেন।",
        "তোমার বাড়ি কোথায়": "আমি ইন্টারনেটে থাকি, তবে তাসনিমের কম্পিউটারে আমার জন্ম।",
        "তোমার নাম কি": "আমার নাম তাসনিম'স চ্যাটবট।",
        "তোমার বয়স কত": "আমি তো সফটওয়্যার, আমার আবার বয়স কিসের!",
        "তুমি কি মানুষ": "না, আমি একজন কৃত্রিম বুদ্ধিমত্তাসম্পন্ন চ্যাটবট।",
        "তুমি কি বন্ধু হবে": "অবশ্যই! আমি আপনার ভার্চুয়াল বন্ধু।",
        "তুমি কি রোবট": "হ্যাঁ, আমি একটি সফটওয়্যার রোবট।",
        "বিয়ে করেছ": "না, আমার বিয়ে করার সুযোগ নেই!",
        "আমাকে চেনো": "আপনি আমার একজন প্রিয় ইউজার, যদিও আমি আপনাকে সামনাসামনি দেখিনি।",

        # --- দৈনন্দিন কাজ ও পরামর্শ ---
        "আজকের দিনটা কেমন": "খুবই চমৎকার! আপনি যদি ইতিবাচক থাকেন তবে দিনটি দারুণ কাটবে।",
        "মন খারাপ": "মন খারাপ করবেন না। একটু গান শুনুন বা বাইরের তাজা বাতাসে ঘুরে আসুন।",
        "ভালো লাগছে না": "চলুন একটু গল্প করি, তাহলে হয়তো ভালো লাগবে। কি নিয়ে কথা বলবেন?",
        "সাহায্য করো": "অবশ্যই! কি ধরনের সাহায্য প্রয়োজন বলুন।",
        "কিভাবে পড়াশোনা করবো": "একটি রুটিন বানিয়ে নিন এবং পড়ার মাঝে ১০ মিনিটের ব্রেক দিন।",
        "ঘুমাতে যাই": "ঠিক আছে, শুভ রাত্রি! ভালো করে ঘুমান।",
        "বিদায়": "বিদায়! আবার কথা হবে, ভালো থাকবেন।",
        "ধন্যবাদ": "আপনাকেও অসংখ্য ধন্যবাদ আমার সাথে কথা বলার জন্য।",
        "হাসি পাচ্ছে না": "একটি জোকস শুনবেন? বল্টু আর তার শিক্ষককে নিয়ে অনেক মজার জোকস আছে আমার কাছে।",
        "কয়টা বাজে": "আপনার ফোনের বা কম্পিউটারের উপরের কোণায় দেখুন, একদম সঠিক সময়টি পেয়ে যাবেন।",

        # --- প্রযুক্তি ও কম্পিউটার ---
        "কম্পিউটার কি": "কম্পিউটার হলো একটি ইলেকট্রনিক যন্ত্র যা তথ্য প্রক্রিয়াকরণ করে।",
        "ইন্টারনেট কি": "ইন্টারনেট হলো বিশ্বজুড়ে ছড়িয়ে থাকা কম্পিউটার নেটওয়ার্কের সমষ্টি।",
        "প্রোগ্রামিং কি": "কম্পিউটারকে কোনো কাজ করানোর জন্য যে ভাষা বা নির্দেশ দেওয়া হয় তাই প্রোগ্রামিং।",
        "সফটওয়্যার কি": "কম্পিউটারের ভেতরে থাকা বিভিন্ন প্রোগ্রাম যা নির্দিষ্ট কাজ সম্পন্ন করে।",
        "হার্ডওয়্যার কি": "কম্পিউটারের বাইরের ভৌত অংশ যা স্পর্শ করা যায়।",
        "পাসওয়ার্ড কি": "পাসওয়ার্ড হলো কোনো অ্যাকাউন্ট সুরক্ষিত রাখার একটি গোপন চাবিকাঠি।",
        "ইউটিউব কি": "একটি ভিডিও শেয়ারিং প্ল্যাটফর্ম যেখানে আপনি সব ধরনের ভিডিও দেখতে পারেন।",
        "ফেসবুক কি": "একটি সামাজিক যোগাযোগ মাধ্যম যেখানে বন্ধুদের সাথে যোগাযোগ রাখা যায়।",

        # --- মজার ও অদ্ভুত প্রশ্ন ---
        "তুমি কি ভূত": "না না! আমি ভূত নই, আমি কেবল একটি কোড মাত্র।",
        "আমাকে একটা গল্প শোনাও": "এক দেশে ছিল এক ছোট চ্যাটবট, সে সবসময় মানুষকে সাহায্য করতে চাইতো...",
        "চাঁদে কি আছে": "চাঁদে শুধু পাথর আর ধুলো আছে, আর আছে মানুষের পায়ের ছাপ।",
        "সূর্য কোথায় যায় রাতে": "সূর্য কোথাও যায় না, পৃথিবী ঘোরে বলে আমরা মনে করি সূর্য ডুবে গেছে।",
        "ভালোবাসা কি": "ভালোবাসা হলো একে অপরের প্রতি শ্রদ্ধা এবং টান।"
    }
        "hi": "Hello! How can I help you?",
        "hello": "Hi there! What's on your mind?",
        "hey": "Hey! I am here to assist you.",
        "assalamualaikum": "Walaikum Assalam! How are you?",
        "আসসালামু আলাইকুম": "ওয়ালাইকুম আসসালাম! আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
        "salam": "Walaikum Assalam!",
        "ki khobor": "Sob bhaloi, apni kemon achen?",
        "kemon acho": "Ami bhalo achi, apni?",
        "how are you": "I am fine, thank you!",
        "kemon achen": "Ji bhalo, dhonnobad.",
        "ki korcho": "Ami apnar sathe kotha bolchi.",
        "what are you doing": "I am processing your requests.",
        "ami bored": "Cholen kotha boli! Tech ba programming niye kisu jigges koren.",
        "tumi ke": "Ami Tasnim er toiri kora ekta chatbot.",
        "who are you": "I am an AI assistant created by Tasnim.",
        "tumar nam ki": "Amar nam Tasnim's Chatbot.",
        "whats your name": "My name is Tasnim's Chatbot.",
        "kisu bolo": "Ki bolbo? Apni kisu jigges koren.",
        "good morning": "Good morning! Have a nice day.",
        "shuvo sokal": "Shuvo sokal! Din ti bhalo katuk.",
        "shuvo ratri": "Shuvo ratri, bhalo ghum hok.",
        "good night": "Good night!",

        # --- Technology & Computer Science ---
        "what is python": "Python is a high-level, interpreted programming language.",
        "python ki": "Python holo ekta khub e popular programming language.",
        "পাইথন কি": "পাইথন একটি শক্তিশালী এবং সহজ প্রোগ্রামিং ভাষা।",
        "what is java": "Java is an object-oriented programming language.",
        "what is html": "HTML is the language used to create web pages.",
        "html ki": "HTML diye website er structure toiri kora hoy.",
        "what is css": "CSS is used to style web pages.",
        "what is ram": "RAM is temporary memory for your computer.",
        "rom ki": "ROM holo permanent memory.",
        "cpu ki": "CPU holo computer er brain.",
        "what is motherboard": "It is the main circuit board of a computer.",
        "software ki": "Software holo kichu instructions er somosthi.",
        "hardware ki": "Computer er vouto ongso gulo holo hardware.",
        "what is internet": "A global network connecting computers worldwide.",
        "wi-fi ki": "Wireless networking technology.",
        "what is ai": "Artificial Intelligence or computer intelligence.",
        "robot ki": "Robot holo ekta programmable machine.",
        "database ki": "Information store korar jaiga.",
        "what is sql": "Language used to manage databases.",
        "cloud computing ki": "Internet er madhyome data store o access kora.",
        "windows ki": "Microsoft er toiri operating system.",
        "linux ki": "Ekta open-source operating system.",

        # --- Lifestyle & General Knowledge ---
        "how to be healthy": "Eat well, exercise, and sleep 8 hours.",
        "sustho thakar upay": "Bhalo khabar khan o protidin bayer koren.",
        "capital of bangladesh": "The capital of Bangladesh is Dhaka.",
        "dhaka ki": "Dhaka holo Bangladesh er rajdhani.",
        "সূর্য কোন দিকে ওঠে": "সূর্য পূর্ব দিকে ওঠে।",
        "sun rises in": "The sun rises in the east.",
        "what is 10+10": "10 + 10 is 20.",
        "১০ যোগ ১০ কত": "১০ যোগ ১০ সমান ২০।",
        "largest river": "The Amazon is the largest river by volume.",
        "podma nodi kothay": "Podma nodi Bangladesh e obosthito.",
        "national fruit of bd": "Jackfruit is the national fruit of Bangladesh.",
        "kathal ki": "Kathal holo Bangladesh er jatiyo fol.",
        "who is the best programmer": "Anyone who solves problems efficiently!",
        "valokore poralekha korar upay": "Monojog diye porun o routine maintain koren.",
        "how to learn english": "Read books and watch movies in English.",
        "tumi ki ranna jano": "Na, ami sudhu kotha bolte jani!",

        # --- Motivational & Helpful ---
        "i am sad": "Don't be sad. Everything will be fine!",
        "mon kharap": "Mon kharap korben na, bhalo kisu chinta koren.",
        "help me": "How can I help you? Please tell me.",
        "amake sahayyo koro": "Ji bolun, ami ki korte pari?",
        "thank you": "You're very welcome!",
        "dhonnobad": "Apnakeo dhonnobad!",
        "bye": "Goodbye! See you soon.",
        "allah hafez": "Allah Hafez! Shuvo biday.",
        "tata": "Tata! Take care.",
        "nice to meet you": "Same here! It was nice talking to you.",
        "tumar sathe kotha bole bhalo laglo": "Amaro khub bhalo laglo.",
        
        # --- Study & Career ---
        "cst ki": "Computer Science and Technology.",
        "diploma engineering ki": "Technical education system.",
        "how to get a job": "Build skills and a good resume.",
        "software engineer kivabe hobo": "Programming shikhen o project toiri koren.",
        "freelancing ki": "Nije mukto vabe kaj kora.",
        "outsourcing ki": "Bairer desh er kaj online e kora.",
        "laptop nite chai": "Budget onujayi bhalo processor dekhe kinun.",
        "best mobile brand": "It depends on your choice, but Xiaomi, Samsung, Apple are popular.",
        
        # --- Adding more variety to fill space ---
        "football": "I love football too, although I can't play!",
        "cricket": "Cricket is a very popular game in Bangladesh.",
        "messi or ronaldo": "Both are legends in their own way.",
        "khabar ki": "Ami to khai na, apni ki kheyechen?",
        "porikkha": "Porikkhar jonno bhalo kore prostuti nin.",
        "exam": "Study hard for your exams!",
        "love": "Love is a beautiful feeling.",
        "valobasha ki": "Valobasha ekta sundor onuvuti.",
        "tumi ki biye korecho": "Na, ami chatbot, amar biye hoy na!",
        "are you married": "No, I am an AI.",
        "funny joke": "Why was the computer cold? Because it left its Windows open!",
        "koutuk": "Boltu: Ma, ami ki boro hoye rasta par hote parbo? Ma: Ha baba. Boltu: Tahole ekhon rasta par hoye dokan theke chocolate niye ashi?",
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
