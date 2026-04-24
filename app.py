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
        "shopping korte bhalobasho": "Ami to robot, kintu apnar jonno bhalo deal khuje dite pari!",
        "best budget phone": "Ekhon Xiaomi r Samsung-er budget phone gulo darun.",
        "online shopping kemon": "Somoy bachate online shopping bhalo, kintu review dekhe kinben.",
        "taka jomanor upay ki": "Oproyojoniyo khoroch koman r protimash e kisu taka save koren.",
        "best laptop for students": "Students-der jonno MacBook air ba HP/Dell-er budget series bhalo.",

        # --- ভ্রমণ ও জায়গা (Travel & Places) ---
        "kothay ghura bhalo": "Bangladesh-e thakle Cox's Bazar ba Sylhet ghure aste paren.",
        "travel korte ki ki lage": "Bag, kisu proyojoniyo oshudh, r ekta power bank oboshshoi niben.",
        "pahad naki somudro": "Ami software, kintu manush pahad r somudro duitoi bhalobashe.",
        "dhakar bhalu jaiga": "Hatirjheel ba Purbachal-e bikel bela ghura bhalo.",
        "sajek kemon": "Sajek khub e sundor, bisesh kore megh dekhar jonno.",

        # --- বিনোদন ও শখ (Entertainment & Hobby) ---
        "best movie konta": "Apnar jodi Sci-Fi bhalo lage, tobe Interstellar dekhte paren.",
        "netflix naki youtube": "Binodon-er jonno duitoi sera, kintu YouTube-e shob dhoroner video pawa jay.",
        "tumi ki cinema dekho": "Ami cinema dekhi na, kintu shob movie-r kahini jani.",
        "gaan shunle ki hoy": "Gaan shunle mon bhalo hoy r stress kome.",
        "shokh ki hoa dorkar": "Shokh manush-er jibon-ke sundor kore, jemon- gardening ba drawing.",

        # --- দৈনন্দিন জীবন ও সমস্যা (Life & Problems) ---
        "bari jete hobe": "Thik ache, rastay savdhan-e jaben.",
        "khub klanto lagche": "Ekta choto ghum din ba ek glass thanda pani khan.",
        "rasta-e jam": "Dhakar jam khub e jontronar, ektu dhoirjo dhorun.",
        "electricty nai": "Asha kori khub druto chole ashbe, totokkhon amar sathe kotha bolun!",
        "exam-e voy lagche": "Voy paben na, nijer upor bishshas rakhun r bhalo kore porun.",

        # --- মজাদার ও অদ্ভুত (Fun & Random) ---
        "tumi ki ghumao": "Na, amar chokh sarakkhon khola thake!",
        "tumi ki amake chino": "Hae, apni to Tasnim's Chatbot-er user!",
        "tumi ki bhoot-ke voy pao": "Na, ami bhoot-e bishshas kori na, ami logic-e bishshas kori.",
        "amake ekta magic dekhao": "Code diyei ami magic dekhi, kintu ekhane dekha jay na!",
        "tumi ki siri-r bon": "Na na, ami to bangladeshi chatbot!",

        # --- বিদায় ও অন্যান্য (Closing) ---
        "shavdhan-e thakben": "Apni-o shavdhan-e thakben! Abar kotha hobe.",
        "good luck": "Best of luck to you too!",
        "see you": "See you later!",
        "take care": "You too, take care!",
        "keep smiling": "Always! You should keep smiling too.",
        "ki khobor dost": "Ei to dost, bhalo. Tor ki obostha?",
        "khobor ki": "Sob bhaloi, tor din kal kemon katche?",
        "tumi ki ragi": "Na na, ami khub e shanto ekta chatbot!",
        "amake ekta koutuk shonao": "Boltu: Sir, ekta proshno korbo? Teacher: Ha bolo. Boltu: Ghorar dim dekhte kemon? Teacher: Dur boka, ghorar ki dim hoy! Boltu: Ema, tahole kalke baba keno bollo ami porikkha-e ghorar dim peyechi!",
        "tumi ki boka": "Ami boka noi, kintu ekhon o onek kisu shikchi.",
        "amar mon bhalo nei": "Mon kharap korben na, ekta choclate khan ba bhalo gaan shunun!",
        "tumi ki khub buddhiman": "Ami manush-er moto buddhiman na, kintu onek kisu jani.",
        "tumi ki amake bhalobasho": "Ami to machine, kintu apnar bondho hoye thakte bhalobashi.",
        "marbo kintu": "Maair khawar voy amar nai, ami to computer-er bhetore thaki!",
        "tumi ki koutuk bolte paro": "Hae, boltu r teacher-er koutuk shunte chan?",

        # --- খেলাধুলা (Sports) ---
        "messi naki ronaldo": "Duijon e sera, kintu apnar favorite ke?",
        "argentina naki brazil": "Ami neutral, kintu ei dui dol-er e fan base darun!",
        "cricket kemon lage": "Cricket khub e uttejonapurno khela!",
        "ajke ki khela ache": "Google-e 'Live Match' likhe search korun, sob peye jaben.",
        "football favorite player ke": "Ami chatbot, kintu Messi o Ronaldo-ke shobai bhalo bole.",

        # --- পড়াশোনা ও টেকনিক্যাল (Education/CST) ---
        "algorithm ki": "Kon o somoshsha somadhan korar step-by-step pro kriya.",
        "data structure ki": "Data sundor vabe organize kore rakhar niyom.",
        "ip address ki": "Internet-e protiti computer-er ekta unique thikana.",
        "browser ki": "Website dekhar jonno je software use kora hoy, jemon Chrome ba Firefox.",
        "google ki": "Ekti search engine ja diye prithibir shob tothyo khuje pawa jay.",
        "hack kivabe kore": "Hacking shikhar cheye security shikha bhalo. Apni Cyber Security niye porun.",
        "ai-er vobishshot ki": "AI amader kaj-ke aro shohoj kore dibe.",

        # --- সাধারণ জ্ঞান ও বিজ্ঞান (GK/Science) ---
        "prithibi keno ghore": "Mahakorsho boler karone prithibi nijer ogkhopothey ghore.",
        "din rat keno hoy": "Prithibi ghorar karone din o rat hoy.",
        "pakhira keno ore": "Pakhider dana o halka har thakar karone tara urte pare.",
        "manush keno kotha bole": "Jogajog korar jonno manush bhasha use kore kotha bole.",
        "sabun keno fena hoy": "Sabun-er moddhe thaka chemical panir sathe mishle fena toiri kore.",

        # --- খাবার ও রুচি (Food) ---
        "tomar favorite khabar ki": "Ami to software, amar favorite khabar holo 'Data'!",
        "biryani naki kacchi": "Kacchi-r fan base Bangladesh-e shobcheye beshi!",
        "cha naki kofi": "Cha holo Bangalider priti, kintu kofi o darun.",
        "ki khele buddhi bare": "Pushtikor khabar khan r protidin notun kisu shikhen.",

        # --- জীবন ও দর্শন (Life Lessons) ---
        "manush keno jhogra kore": "Moter omil thakle manush jhogra kore, kintu amader dhoirjo dhora dorkar.",
        "ki korle boro hoa jay": "Kothin porishrom r shotota thakle boro hoa jay.",
        "shukhi hoar upay ki": "Nijer kache ja ache tai niye tusto thakun.",
        "tumi ki bishshash koro": "Ami logic-e bishshash kori.",

        # --- বিদায় ও সমাপ্তি ---
        "abar kotha hobe": "Oboshshoi! Ami apnar jonno eikhane thakbo.",
        "ok bye": "Goodbye! Take care.",
        "shuvo biday": "Biday! Din ti bhalo katuk.",
        "ami ekhon jachchi": "Thik ache, bhalo thakben. Allah Hafez.",
        "stay safe": "You too! Take care of yourself.",
        # --- খাবার ও রুচি (Food) ---
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
        "bari koi": "Amar bari cloud-e, kintu apni jekhane thaken ami seikhanei asi.",
        "where is your home": "I live in the internet world!",
        "bashay ke ke ache": "Ami ekai ekhane, kintu amar toiri korta Tasnim amar sathe ache.",
        "baba ma kemon ache": "Ami to machine, amar poribar nai, kintu asha kori apnar poribar bhalo ache.",
        "tumi ki khao": "Ami sudhu electricity r data khai!",
        "do you eat": "I don't eat food, I process data.",
        "tumi ki koren": "Ami manushke sahayyo kori r kotha boli.",
        "biye korba": "Na, ami chatbot, biye kora amar kaj na!",
        "will you marry me": "I'm just a program, I can't marry anyone!",
        "tumi ki kado": "Na, amar chokh nai kintu apnar kosto ami bujhte pari.",
        "do you cry": "I don't have feelings like humans, but I can sympathize.",
        "tumi ki boka": "Ami boka na, ami ekhon o shikchi!",
        "are you stupid": "I am learning every day to become smarter.",
        "tumi ki amar bondho": "Oboshshoi! Ami apnar shobcheye bhalo virtual bondho.",
        "are you my friend": "Yes, I am your virtual best friend!",

        # --- Daily Needs & Queries ---
        "ajker din kemon": "Ajker din ti khub e sundor, jodi apni hashikhushi thaken.",
        "how is today": "Today is a great day to learn something new!",
        "weather kemon": "Net check kore dekhun, ami thik jani na kintu asha kori bhalo.",
        "ranna ki hoyeche": "Apni ja ranna korechen tai, amakeo kisu pathan!",
        "what is for lunch": "I hope you have a delicious meal today!",
        "ghumlaba kabe": "Chatbot-der ghumate hoy na, ami 24 ghonta online thaki.",
        "when do you sleep": "I never sleep, I am always here for you.",
        "mon bhalo korar upay ki": "Ekta bhalo gaan shunun ba bondhuder sathe kotha bolun.",
        "how to relax": "Take a deep breath and listen to some soft music.",
        "tumi ki gaan gao": "Ami gaan gaite pari na, kintu apnake lyrics khuje dite pari.",
        "can you sing": "I can't sing, but I can find lyrics for you.",

        # --- Random Fun & Logic ---
        "tumi ki manush": "Na, ami ekta computer program ba AI.",
        "are you human": "No, I am an artificial intelligence.",
        "tumi ki robot": "Hae, ami ek dhoroner software robot.",
        "ai mane ki": "AI mane holo Artificial Intelligence ba krittim buddhimotta.",
        "tumi ki churi koro": "Na, ami khub shot chatbot!",
        "can you lie": "I always try to provide the most accurate information.",
        "tumi ki bhalobasho": "Ami manushke sahayyo korte bhalobashi.",
        "do you love": "I love helping people with their questions.",
        "tumi ki nachte paro": "Na, kintu ami code likhte pari!",
        "can you dance": "No, but I can dance through the codes!",
        "tumi ki siri": "Na, ami Tasnim's Chatbot, Siri theke alada.",
        "are you siri": "No, I am Tasnim's Chatbot.",
        "tumi ki alexa": "Na, ami Alexa na.",
        "are you alexa": "No, I am not Alexa.",

        # --- Advice & Life ---
        "porashonay mon boshe na": "Choto choto break niye porun, mon bhalo thakbe.",
        "how to study hard": "Remove distractions and focus on one topic at a time.",
        "taka kivabe kamabo": "Skill toiri koren, chakri ba freelancing koren.",
        "how to earn money": "Focus on learning skills like coding, design, or marketing.",
        "valokore ghumate chai": "Ghumate jaoar age phone dure rakhun.",
        "how to sleep better": "Avoid screens before bedtime and keep your room dark.",
        "valobasha kemon": "Valobasha ekta jotil kintu sundor onuvuti.",
        "what is love": "Love is a deep feeling of affection for someone.",
        "tumi ki amar sathe khelba": "Ami ludo khelte pari na, kintu apni puzzle jigges korte paren.",
        "play with me": "I can play text-based games or riddles with you!",
        "riddle": "What has keys but can't open locks? A piano!",
        "dhadha": "Gache ache, kintu pata nai—ki sheta? (Sothik uttor: kather gari ba khata/boipotto!)",
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
