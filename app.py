import os
import base64
import streamlit as st
import google.generativeai as genai

# Ambil API Key dari secrets
api_key = st.secrets["GEMINI_API_KEY"]


# Konfigurasi Gemini
genai.configure(api_key=api_key)

GEMINI_MODEL = "gemini-2.5-flash"

# Fungsi helper
def extract_text(resp):
    try:
        candidates = resp.candidates or []
        if candidates and candidates[0].content.parts:
            return candidates[0].content.parts[0].text
        return str(resp)
    except Exception as e:
        return str(resp)

st.title("🎨 Gemini AI Playground (Streamlit)")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Text", "🖼️ Gambar", "📄 Dokumen", "🎵 Audio"])

# 1. Text
with tab1:
    prompt = st.text_area("Masukkan perintah:")
    if st.button("Kirim Perintah"):
        if prompt.strip():
            model = genai.GenerativeModel(GEMINI_MODEL)
            resp = model.generate_content(prompt)
            st.subheader("Hasil:")
            st.write(extract_text(resp))

# 2. Image
with tab2:
    prompt = st.text_area("Perintah untuk gambar:")
    image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if st.button("Kirim Perintah"):
        if image_file and prompt.strip():
            image_data = image_file.read()
            model = genai.GenerativeModel(GEMINI_MODEL)
            resp = model.generate_content([
                prompt,
                {
                    "mime_type": image_file.type,
                    "data": base64.b64encode(image_data).decode("utf-8")
                }
            ])
            st.subheader("Hasil:")
            st.write(extract_text(resp))

# 3. Document
with tab3:
    prompt = st.text_area("Perintah untuk dokumen:", value="Tolong buatkan ringkasan dari dokumen berikut.")
    doc_file = st.file_uploader("Upload Document", type=["pdf", "txt", "docx"])
    if st.button("Kirim Perintah"):
        if doc_file:
            doc_data = doc_file.read()
            model = genai.GenerativeModel(GEMINI_MODEL)
            resp = model.generate_content([
                prompt,
                {
                    "mime_type": doc_file.type,
                    "data": base64.b64encode(doc_data).decode("utf-8")
                }
            ])
            st.subheader("Hasil:")
            st.write(extract_text(resp))

# 4. Audio
with tab4:
    prompt = st.text_area("Perintah untuk audio:", value="Ubah menjadi tulisan audio berikut.")
    audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
    if st.button("Kirim Perintah"):
        if audio_file:
            audio_data = audio_file.read()
            model = genai.GenerativeModel(GEMINI_MODEL)
            resp = model.generate_content([
                prompt,
                {
                    "mime_type": audio_file.type,
                    "data": base64.b64encode(audio_data).decode("utf-8")
                }
            ])
            st.subheader("Hasil:")
            st.write(extract_text(resp))
