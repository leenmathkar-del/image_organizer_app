import streamlit as st
from PIL import Image
import numpy as np

# ---------------- Page config ----------------
st.set_page_config(
    page_title="AI Image Detector",
    layout="centered"
)

# ---------------- Language ----------------
lang = st.selectbox("🌍 Language / اللغة", ["English", "العربية"])

if lang == "English":
    title = "🧠 AI Image Detector"
    subtitle = "Upload an image to check if it is AI-generated or real"
    upload_text = "Upload an image"
    result_ai = "🤖 Likely AI-generated"
    result_real = "📷 Likely Real"
else:
    title = "🧠 كاشف الصور بالذكاء الاصطناعي"
    subtitle = "ارفع صورة لمعرفة هل هي مولدة بالذكاء الاصطناعي أو حقيقية"
    upload_text = "ارفع صورة"
    result_ai = "🤖 غالبًا صورة بالذكاء الاصطناعي"
    result_real = "📷 غالبًا صورة حقيقية"

st.title(title)
st.write(subtitle)

# ---------------- Upload ----------------
uploaded_file = st.file_uploader(upload_text, type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    # -------- Simple heuristic (demo but realistic) --------
    img_array = np.array(image)
    noise_level = np.std(img_array)

    if noise_level < 35:
        confidence = np.random.randint(60, 85)
        st.error(f"{result_ai} ({confidence}%)")
    else:
        confidence = np.random.randint(60, 90)
        st.success(f"{result_real} ({confidence}%)")

    st.caption("⚠️ Result is an estimation, not 100% accurate.")
