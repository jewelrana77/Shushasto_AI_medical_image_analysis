import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st

# Set your API Key (Replace with your actual key)
GOOGLE_API_KEY = "AIzaSyBg32ilqafq1F4ObgDDSscWp8q4DT2nv_g"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Ensure API Key is provided
if not GOOGLE_API_KEY:
    raise ValueError("⚠️ Please set your Google API Key in GOOGLE_API_KEY")

# Initialize the Medical Agent
medical_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

query = """
তুমি একজন অত্যন্ত দক্ষ মেডিকেল ইমেজিং বিশেষজ্ঞ, রেডিওলজি ও ডায়াগনস্টিক ইমেজিং-এ পারদর্শী। প্রদত্ত মেডিকেল ছবিটি বিশ্লেষণ করো এবং নিচের কাঠামো অনুযায়ী উত্তর দাও:

### ১. ইমেজের ধরন ও অঞ্চল
- কোন ইমেজিং পদ্ধতি ব্যবহার হয়েছে (এক্স-রে/এমআরআই/সিটি/আল্ট্রাসাউন্ড ইত্যাদি)।
- কোন অঙ্গ বা অঞ্চলের ছবি এটি।
- ইমেজের গুণমান ও প্রযুক্তিগত দিক বিশ্লেষণ করো।

### ২. প্রধান পর্যবেক্ষণ
- মূল দৃশ্যমান বৈশিষ্ট্যগুলো বর্ণনা করো।
- সম্ভাব্য অস্বাভাবিকতা থাকলে বিশদভাবে উল্লেখ করো।
- প্রয়োজন হলে মাপ বা ঘনত্ব উল্লেখ করো।

### ৩. ডায়াগনস্টিক মূল্যায়ন
- সম্ভাব্য প্রধান রোগ নির্ণয় ও আত্মবিশ্বাসের মাত্রা উল্লেখ করো।
- সম্ভাব্য অন্যান্য রোগের তালিকা দাও, সম্ভাবনার ক্রম অনুযায়ী।
- প্রতিটি নির্ণয়ের যুক্তি সংক্ষেপে ব্যাখ্যা করো।
- জরুরি বা গুরুতর ফলাফল থাকলে বিশেষভাবে উল্লেখ করো।

### ৪. রোগী-বান্ধব ব্যাখ্যা
- সহজ ভাষায় ফলাফল ব্যাখ্যা করো।
- জটিল চিকিৎসা পরিভাষার সহজ ব্যাখ্যা দাও।
- প্রয়োজনে তুলনামূলক উদাহরণ ব্যবহার করো।

### ৫. গবেষণা প্রেক্ষাপট
- DuckDuckGo সার্চ ব্যবহার করে সাম্প্রতিক গবেষণা খুঁজে বের করো।
- প্রমিত চিকিৎসা প্রোটোকল অনুসন্ধান করো।
- বিশ্লেষণকে সমর্থন করে এমন ২–৩টি মূল রেফারেন্স দাও।

উত্তরটি গঠনমূলক ও চিকিৎসা-সংক্রান্তভাবে সঠিক হতে হবে, স্পষ্ট markdown ফরম্যাটে দাও।
"""


# Function to analyze medical image
def analyze_medical_image(image_path):
    """মেডিকেল ইমেজ বিশ্লেষণ"""
    
    # Open and resize image
    image = PILImage.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    new_width = 500
    new_height = int(new_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))

    # Save resized image
    temp_path = "temp_resized_image.png"
    resized_image.save(temp_path)

    # Create AgnoImage object
    agno_image = AgnoImage(filepath=temp_path)

    # Run AI analysis
    try:
        response = medical_agent.run(query, images=[agno_image])
        return response.content
    except Exception as e:
        return f"⚠️ Analysis error: {e}"
    finally:
        # Clean up temporary file
        os.remove(temp_path)


# Streamlit UI setup
st.set_page_config(page_title="Medical Image Analysis", layout="centered")
st.title("🩺 Shushasto.AI মেডিকেল ইমেজ বিশ্লেষণ টুল 🔬")
st.markdown(
    """
    স্বাগতম **Shushasto.AI মেডিকেল ইমেজ বিশ্লেষণ** টুলে! 📸  
    এখানে আপনি এক্স-রে, এমআরআই, সিটি স্ক্যান, বা আল্ট্রাসাউন্ডসহ যেকোনো চিকিৎসা-সংক্রান্ত ছবি আপলোড করতে পারেন।  
    আমাদের Shushasto.AI-চালিত সিস্টেম ছবিটি বিশ্লেষণ করে বিস্তারিত ফলাফল, সম্ভাব্য রোগ নির্ণয় এবং গবেষণা-ভিত্তিক অন্তর্দৃষ্টি প্রদান করবে।  
    চলুন শুরু করা যাক!
    """
)



# Upload image section
st.sidebar.header("আপনার মেডিকেল ইমেজ আপলোড করুন:")
uploaded_file = st.sidebar.file_uploader("একটি মেডিকেল ইমেজ ফাইল নির্বাচন করুন", type=["jpg", "jpeg", "png", "bmp", "gif"])

# Button to trigger analysis
if uploaded_file is not None:
    # Display the uploaded image in Streamlit
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    if st.sidebar.button("Analyze Image"):
        with st.spinner("🔍 ইমেজ বিশ্লেষণ করা হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।"):
            # Save the uploaded image to a temporary file
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Run analysis on the uploaded image
            report = analyze_medical_image(image_path)
            
            # Display the report
            st.subheader("📋 বিশ্লেষণ প্রতিবেদন")
            st.markdown(report, unsafe_allow_html=True)
            
            # Clean up the saved image file
            os.remove(image_path)
else:
    st.warning("⚠️ অনুগ্রহ করে বিশ্লেষণ শুরু করতে একটি মেডিকেল ইমেজ আপলোড করুন।")
