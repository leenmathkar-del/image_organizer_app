 import streamlit as st
from PIL import Image, ImageFilter
import numpy as np

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="AI Image Detector | كاشف الصور",
    page_icon="🧠",
    layout="centered"
)

# -----------------------
# Language selector
# -----------------------
lang = st.selectbox("🌍 Language / اللغة", ["العربية", "English"])

TEXT = {
    "العربية": {
        "title": "🧠 كاشف الصور بالذكاء الاصطناعي",
        "desc": "ارفع صورة وسيتم تحليلها لمعرفة هل هي حقيقية أم مولدة بالذكاء الاصطناعي",
        "upload": "📤 ارفع صورة",
        "real": "📸 صورة حقيقية",
        "ai": "🤖 صورة مولدة بالذكاء الاصطناعي",
        "confidence": "نسبة الثقة",
        "footer": "⚠️ النتيجة تقديرية وليست 100٪ دقيقة"
    },
    "English": {
        "title": "🧠 AI Image Detector",
        "desc": "Upload an image to check whether it is real or AI-generated",
        "upload": "📤 Upload Image",
        "real": "📸 Real Image",
        "ai": "🤖 AI Generated Image",
        "confidence": "Confidence",
        "footer": "⚠️ Results are estimations, not 100% accurate"
    }
}

t = TEXT[lang]

# -----------------------
# UI
# -----------------------
st.title(t["title"])
st.write(t["desc"])

uploaded_file = st.file_uploader(
    t["upload"],
    type=["jpg", "jpeg", "png"]
)

# -----------------------
# Detection logic (NO cv2)
# -----------------------
def detect_ai(image):
    gray = image.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)

    arr = np.array(edges)
    sharpness = arr.var()

    if sharpness < 150:
        label = "AI"
        confidence = int(min(95, 100 - sharpness))
    else:
        label = "REAL"
        confidence = int(min(95, sharpness / 2))

    return label, confidence

# -----------------------
# Result
# -----------------------
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    label, confidence = detect_ai(image)

    st.markdown("---")

    if label == "AI":
        st.error(t["ai"])
    else:
        st.success(t["real"])

    st.metric(t["confidence"], f"{confidence}%")
    st.caption(t["footer"])
