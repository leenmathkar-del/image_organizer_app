import streamlit as st
import os
import shutil

FOUND = "found_images"
LOST = "lost_images"

os.makedirs(FOUND, exist_ok=True)
os.makedirs(LOST, exist_ok=True)

st.title("📸 موقع تنظيم الصور")

uploaded_files = st.file_uploader(
    "ارفع الصور",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

def organize_images(files):
    moved = 0
    for file in files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())

        if "7116" in file.name:
            dest = os.path.join(LOST, file.name)
        else:
            dest = os.path.join(FOUND, file.name)

        shutil.move(file.name, dest)
        moved += 1
    return moved

if st.button("🚀 نظّم الصور"):
    if uploaded_files:
        total = organize_images(uploaded_files)
        st.success(f"تم تنظيم {total} صورة ✅")
    else:
        st.warning("ارفع صور أولاً")
