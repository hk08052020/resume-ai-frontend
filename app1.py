import streamlit as st
import requests
from io import BytesIO
from typing import Tuple
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="AI Resume & Cover Letter", page_icon="🧾", layout="wide")
st.title("🧾 AI Resume & Cover Letter Generator")

st.caption("Upload your resume and paste a job description. This app calls your secure backend on Render.")

# ---- Backend URL ----
default_backend = st.secrets.get("BACKEND_URL", "")
backend_url = st.text_input("Backend URL (from Render)", value=default_backend, placeholder="https://resume-ai-backend.onrender.com")
if not backend_url:
    st.info("Enter your backend URL (ending in .onrender.com).")

tone = st.selectbox("Cover letter
