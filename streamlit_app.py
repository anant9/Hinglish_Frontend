
# ===========================
# 📁 streamlit_app.py
# ===========================
import requests
import streamlit as st
from dotenv import load_dotenv
#from services.srt_processor import process_srt
#from services.gemini_client import transliterate_batch
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🎬 Hindi to Hinglish Subtitle Converter")

# ---- Google Login ----
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None

if st.session_state.jwt_token:
    st.success("✅ Logged in!")
else:
    st.info("🔐 Please login with Google first.")
    login_url = f"{BACKEND_URL}/login"
    if st.button("Login with Google"):
        st.markdown(f"[Login Here]({login_url})", unsafe_allow_html=True)

query_params = st.query_params
if "token" in query_params:
    st.session_state.jwt_token = query_params["token"]
    st.query_params.clear()
    st.rerun()

# ---- Subtitle Upload ----
if st.session_state.jwt_token:
    uploaded_file = st.file_uploader("Upload Hindi .srt File", type=["srt"])

    if uploaded_file:
        st.write("📤 Sending file to backend for transliteration...")

        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")}
            response = requests.post(f"{BACKEND_URL}/generate_subtitles", files=files)

            if response.status_code == 200:
                result = response.json()
                converted_content = result.get("converted_srt", "")

                st.download_button(
                    "⬇️ Download Hinglish Subtitles",
                    data=converted_content,
                    file_name="hinglish_subtitles.srt",
                    mime="text/plain"
                )
            else:
                st.error(f"Error from backend: {response.status_code} {response.text}")

        except Exception as e:
            st.error(f"Error calling backend: {e}")

