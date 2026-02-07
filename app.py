import streamlit as st
import requests
from PIL import Image
import io

# --------- PUT YOUR KEYS HERE ----------
API_USER = "1646868698"
API_SECRET = "zzHsRe8fz2f9bSh8aKFNSUJy2gBGYSBu"
# --------------------------------------

st.set_page_config(page_title="AI Image Detector", layout="centered")

lang = st.selectbox("🌍 Language / اللغة", ["English", "العربية"])

if lang == "English":
    st.title("🧠 AI Image Detector")
    st.write("Upload an image to check if it is AI-generated")
    upload_text = "Upload image"
else:
    st.title("🧠 كاشف الصور بالذكاء الاصطناعي")
    st.write("ارفع صورة لمعرفة هل هي مولدة بالذكاء الاصطناعي")
    upload_text = "ارفع صورة"

file = st.file_uploader(upload_text, type=["jpg", "jpeg", "png"])

if file:
    image = Image.open(file)
    st.image(image, use_column_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes = img_bytes.getvalue()

    response = requests.post(
        "https://api.sightengine.com/1.0/check.json",
        files={"media": img_bytes},
        data={
            "models": "genai",
            "api_user": API_USER,
            "api_secret": API_SECRET
        }
    )

    result = response.json()

    if "type" in result:
        ai_score = result["type"]["ai_generated"] * 100
        real_score = 100 - ai_score

        if ai_score > 50:
            st.error(f"🤖 AI Generated: {ai_score:.1f}%")
        else:
            st.success(f"📷 Real Image: {real_score:.1f}%")
    else:
        st.warning("Could not analyze this image.")
