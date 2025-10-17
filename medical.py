import os
import re
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st
from gtts import gTTS
import base64

# Set your API Key
GOOGLE_API_KEY = "AIzaSyBg32ilqafq1F4ObgDDSscWp8q4DT2nv_g"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

if not GOOGLE_API_KEY:
    raise ValueError("⚠️ Please set your Google API Key in GOOGLE_API_KEY")

# Initialize the Medical Agent
medical_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

query = """
তুমি একজন বিশেষজ্ঞ রেডিওলজিস্ট এবং মেডিকেল ইমেজিং বিশেষজ্ঞ। প্রদত্ত মেডিকেল ইমেজটি পেশাদার এবং বিস্তারিতভাবে বিশ্লেষণ করো।

**গুরুত্বপূর্ণ নির্দেশনা:**
- কোনো ভূমিকা বা সূচনা বাক্য ছাড়াই সরাসরি বিশ্লেষণ শুরু করো
- "ঠিক আছে", "দেওয়া ছবিটি", বা এই ধরনের কোনো শুরুর কথা লিখবে না
- পেশাদার এবং চিকিৎসা-সংক্রান্তভাবে সঠিক তথ্য প্রদান করো
- বাংলায় স্পষ্ট এবং সহজবোধ্য ভাষা ব্যবহার করো

---

## ১. ইমেজিং পরিচিতি

**ইমেজের ধরন ও পদ্ধতি:**
- কোন ইমেজিং মোডালিটি ব্যবহৃত হয়েছে (X-ray/CT/MRI/Ultrasound/PET ইত্যাদি)
- কোন এনাটমিক্যাল অঞ্চল বা অঙ্গের স্ক্যান
- ভিউ/প্রজেকশন (AP/PA/Lateral/Axial/Sagittal/Coronal ইত্যাদি)
- ইমেজ কোয়ালিটি মূল্যায়ন (exposure, positioning, artifacts)

---

## ২. পর্যবেক্ষণ ও ফাইন্ডিংস

**স্বাভাবিক শারীরবৃত্তীয় বৈশিষ্ট্য:**
- যে অংশগুলো স্বাভাবিক দেখাচ্ছে তা উল্লেখ করো

**অস্বাভাবিক বা উল্লেখযোগ্য ফাইন্ডিংস:**
- প্রতিটি অস্বাভাবিকতার বিস্তারিত বর্ণনা
- অবস্থান, আকার, আকৃতি, ঘনত্ব/ইন্টেনসিটি
- সংখ্যা (একক বা মাল্টিপল লেশন)
- পার্শ্ববর্তী টিস্যুতে প্রভাব

**প্যাথোলজিক্যাল সাইন:**
- কোনো ক্লাসিক রেডিওলজিক্যাল সাইন দৃশ্যমান কিনা

---

## ৩. ডায়াগনস্টিক মূল্যায়ন

**প্রাথমিক/সম্ভাব্য ডায়াগনসিস:**
- মূল রোগ নির্ণয় (১-২টি সবচেয়ে সম্ভাব্য)
- প্রতিটির confidence level (High/Moderate/Low)
- ডায়াগনসিসের পক্ষে যুক্তি ও সাপোর্টিং ফাইন্ডিংস

**ডিফারেনশিয়াল ডায়াগনসিস:**
- অন্যান্য সম্ভাব্য রোগ (৩-৪টি, সম্ভাবনার ক্রমানুসারে)
- প্রতিটির সংক্ষিপ্ত ব্যাখ্যা

**সিভিয়ারিটি অ্যাসেসমেন্ট:**
- রোগের তীব্রতা (Mild/Moderate/Severe)
- জরুরি চিকিৎসা প্রয়োজন কিনা

---

## ৪. সহজ ভাষায় ব্যাখ্যা

**রোগীর জন্য সরল ভাষায়:**
- কী দেখা যাচ্ছে তা সহজ উদাহরণ দিয়ে বুঝাও
- জটিল মেডিকেল টার্মের বাংলা ব্যাখ্যা
- তুলনামূলক উপমা ব্যবহার করো (যেমন: "ফুসফুসে পানি জমা যেমন...")

**সম্ভাব্য কারণ:**
- কেন এই অবস্থা হতে পারে (জীবনযাপন/জেনেটিক/ইনফেকশন ইত্যাদি)

**পরবর্তী পদক্ষেপ:**
- কী ধরনের চিকিৎসা প্রয়োজন হতে পারে
- আরও কোন পরীক্ষা করা উচিত

---

## ৫. ক্লিনিক্যাল সুপারিশ

**প্রস্তাবিত ফলো-আপ:**
- অতিরিক্ত ইমেজিং (যদি প্রয়োজন হয়)
- ল্যাবরেটরি পরীক্ষা
- স্পেশালিস্ট রেফারেল

**সতর্কতা:**
- কোন লক্ষণে তাৎক্ষণিক চিকিৎসকের পরামর্শ নিতে হবে

---

## ৬. রেফারেন্স ও গবেষণা

DuckDuckGo সার্চ ব্যবহার করে:
- এই কন্ডিশন সম্পর্কিত সাম্প্রতিক গাইডলাইন
- প্রমাণভিত্তিক চিকিৎসা প্রোটোকল
- নির্ভরযোগ্য মেডিকেল সোর্স থেকে ২-৩টি রেফারেন্স

---

**দাবিত্যাগ:** এই বিশ্লেষণ শুধুমাত্র তথ্যমূলক। পেশাদার চিকিৎসা পরামর্শের বিকল্প নয়। নিশ্চিত রোগ নির্ণয় ও চিকিৎসার জন্য অবশ্যই যোগ্য চিকিৎসকের সাথে পরামর্শ করুন।
"""


def clean_text_for_speech(text):
    """টেক্সট থেকে markdown এবং বিশেষ চিহ্ন সরিয়ে পরিষ্কার করে"""
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = text.strip()
    return text


def text_to_speech(text, lang='bn', slow=False):
    """টেক্সট থেকে অডিও তৈরি করে (gTTS)"""
    try:
        clean_text = clean_text_for_speech(text)
        
        if not clean_text or len(clean_text.strip()) < 10:
            return None
        
        tts = gTTS(text=clean_text, lang=lang, slow=slow)
        audio_file = "output_audio.mp3"
        tts.save(audio_file)
        
        if os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
            return audio_file
        else:
            return None
            
    except Exception as e:
        st.error(f"অডিও তৈরিতে সমস্যা হয়েছে। দয়া করে আবার চেষ্টা করুন।")
        return None


def autoplay_audio(file_path):
    """অডিও অটো-প্লে করার জন্য HTML তৈরি করে"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay style="width: 100%; margin-top: 10px;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        pass


def analyze_medical_image(image_path):
    """মেডিকেল ইমেজ বিশ্লেষণ"""
    image = PILImage.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    temp_path = "temp_resized_image.png"
    resized_image.save(temp_path)
    agno_image = AgnoImage(filepath=temp_path)

    try:
        response = medical_agent.run(query, images=[agno_image])
        
        if hasattr(response, 'content'):
            result = response.content
        elif isinstance(response, str):
            result = response
        else:
            result = str(response)
        
        if not result or result.strip() == "":
            return "⚠️ কোনো বিশ্লেষণ ফলাফল পাওয়া যায়নি।"
        
        return result
        
    except Exception as e:
        return f"⚠️ বিশ্লেষণে সমস্যা হয়েছে। দয়া করে আবার চেষ্টা করুন।"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# Custom CSS for beautiful, modern design
st.set_page_config(
    page_title="Shushasto.AI | Medical Imaging Analysis", 
    layout="wide", 
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container with animated gradient */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 2rem;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header with glassmorphism */
    .main-header {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 3rem 2rem;
        border-radius: 30px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        font-size: 1rem;
        margin-top: 0.8rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Card styling with glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin: 1.5rem 0;
        transition: all 0.4s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        border-color: rgba(255, 255, 255, 0.6);
    }
    
    /* Upload section styling */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px dashed rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Image container with elegant border */
    .image-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
        margin: 2rem 0;
        border: 3px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .image-container:hover {
        transform: scale(1.02);
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Checkbox styling */
    .stCheckbox {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Report section */
    .report-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        margin-top: 2rem;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    .report-section h2 {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 1.5rem;
        font-size: 2rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Section headers */
    h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.4rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.2) 100%);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .info-card h3 {
        margin-top: 0;
        font-size: 1.5rem;
    }
    
    .info-card ul, .info-card ol {
        line-height: 2;
        font-size: 1rem;
    }
    
    /* Audio player */
    audio {
        width: 100%;
        margin-top: 1.5rem;
        border-radius: 15px;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.2rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: white !important;
        border-right-color: transparent !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2.5rem;
        color: white;
        font-size: 0.95rem;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .footer b {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Text styling */
    p {
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
    }
    
    /* Markdown content in report */
    .report-section p, .report-section li {
        color: #333;
        line-height: 1.9;
    }
    
    .report-section strong {
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🏥 Shushasto.AI</h1>
        <p>Advanced Medical Imaging Analysis Platform</p>
        <p class="subtitle">Powered by AI • বাংলা ভয়েস সাপোর্ট • Real-time Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📤 আপলোড সেকশন")
    uploaded_file = st.file_uploader(
        "মেডিকেল ইমেজ সিলেক্ট করুন",
        type=["jpg", "jpeg", "png", "bmp", "gif"],
        help="এক্স-রে, এমআরআই, সিটি স্ক্যান, বা আল্ট্রাসাউন্ড ইমেজ আপলোড করুন"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(uploaded_file, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ সেটিংস")
        enable_audio = st.checkbox("🔊 অডিও রিপোর্ট সক্রিয় করুন", value=True)
        auto_play = st.checkbox("▶️ অটো-প্লে সক্রিয় করুন", value=False)
        slow_speech = st.checkbox("🐢 ধীর গতির অডিও", value=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        analyze_button = st.button("🔬 বিশ্লেষণ শুরু করুন", type="primary", use_container_width=True)
    else:
        st.info("👆 একটি মেডিকেল ইমেজ আপলোড করুন")
        analyze_button = False

with col2:
    if uploaded_file and analyze_button:
        with st.spinner("🔍 ইমেজ বিশ্লেষণ করা হচ্ছে..."):
            # Save uploaded image
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Analyze image
            report = analyze_medical_image(image_path)
            
            # Display report
            if report and len(report) > 10:
                st.markdown('<div class="report-section">', unsafe_allow_html=True)
                st.markdown("## 📋 বিশ্লেষণ প্রতিবেদন")
                st.markdown(report, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Generate audio if enabled
                if enable_audio:
                    with st.spinner("🎙️ অডিও রিপোর্ট তৈরি হচ্ছে..."):
                        audio_file = text_to_speech(report, lang='bn', slow=slow_speech)
                        
                        if audio_file and os.path.exists(audio_file):
                            st.success("✅ অডিও রিপোর্ট প্রস্তুত")
                            
                            with open(audio_file, 'rb') as f:
                                audio_bytes = f.read()
                            
                            if auto_play:
                                autoplay_audio(audio_file)
                            else:
                                st.audio(audio_bytes, format='audio/mp3')
                            
                            try:
                                os.remove(audio_file)
                            except:
                                pass
            else:
                st.error("⚠️ বিশ্লেষণ ফলাফল পাওয়া যায়নি")
            
            # Clean up
            try:
                os.remove(image_path)
            except:
                pass
    elif not uploaded_file:
        st.markdown("""
            <div class="info-card">
                <h3>🎯 কীভাবে ব্যবহার করবেন</h3>
                <ol>
                    <li>বাম দিক থেকে একটি মেডিকেল ইমেজ আপলোড করুন</li>
                    <li>প্রয়োজনীয় সেটিংস নির্বাচন করুন</li>
                    <li>"বিশ্লেষণ শুরু করুন" বাটনে ক্লিক করুন</li>
                    <li>AI-ভিত্তিক বিশ্লেষণ পান বাংলায়</li>
                </ol>
            </div>
            
            <div class="info-card">
                <h3>✨ ফিচারসমূহ</h3>
                <ul>
                    <li>🤖 <b>AI-Powered Analysis</b> - Google Gemini দ্বারা চালিত</li>
                    <li>🔊 <b>বাংলা ভয়েস</b> - রিপোর্ট শুনুন বাংলায়</li>
                    <li>📚 <b>Research Integration</b> - সাম্প্রতিক গবেষণা রেফারেন্স</li>
                    <li>🎯 <b>Professional Report</b> - বিস্তারিত ডায়াগনস্টিক রিপোর্ট</li>
                </ul>
            </div>
            
            <div class="info-card">
                <h3>⚠️ গুরুত্বপূর্ণ নোট</h3>
                <p>
                এই টুলটি শুধুমাত্র তথ্যমূলক উদ্দেশ্যে। এটি পেশাদার চিকিৎসা পরামর্শ, 
                রোগ নির্ণয় বা চিকিৎসার বিকল্প নয়। সর্বদা যোগ্য স্বাস্থ্যসেবা পেশাদারের 
                পরামর্শ নিন।
                </p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p><b>Shushasto.AI</b> © 2025 | AI-Powered Medical Imaging Analysis</p>
        <p style="font-size: 0.9rem; margin-top: 0.8rem; opacity: 0.9;">
            Powered by Alpha_JR • Made with ❤️ for Healthcare
        </p>
    </div>
    """, unsafe_allow_html=True)
