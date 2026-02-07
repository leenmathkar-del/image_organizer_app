import streamlit as st
from PIL import Image
import numpy as np
import cv2

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

# -----------------------
# Texts
# -----------------------
TEXT = {
    "العربية": {
        "title": "🧠 كاشف الصور بالذكاء الاصطناعي",
        "desc": "ارفع صورة وسيتم تحليلها لمعرفة هل هي حقيقية أم مولدة بالذكاء الاصطناعي",
        "upload": "📤 ارفع صورة",
        "real": "📸 صورة حقيقية",
        "ai": "🤖 صورة مولدة بالذكاء الاصطناعي",
        "confidence": "نسبة الثقة",
        "footer": "النتيجه تقريبيه ليست دقيقه"
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
# Title
# -----------------------
st.title(t["title"])
st.write(t["desc"])

# -----------------------
# Upload image
# -----------------------
uploaded_file = st.file_uploader(
    t["upload"],
    type=["jpg", "jpeg", "png"]
)

# -----------------------
# Detection logic
# -----------------------
def detect_ai(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Laplacian variance (blur / smoothness)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Heuristic decision
    if variance < 120:
        label = "AI"
        confidence = min(95, int(100 - variance))
    else:
        label = "REAL"
        confidence = min(95, int(variance / 2))

    return label, confidence

# -----------------------
# Show result
# -----------------------
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    label, confidence = detect_ai(image)

    st.markdown("---")

    if label == "AI":
        st.error(f"{t['ai']}")
    else:
        st.success(f"{t['real']}")

    st.metric(t["confidence"], f"{confidence}%")

    st.caption(t["footer"])
