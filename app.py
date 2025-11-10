import streamlit as st
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

# ---------- Page setup ----------
st.set_page_config(page_title="AI Resume & Cover Letter", page_icon="🧾", layout="wide")
st.title("🧾 AI Resume & Cover Letter Generator")
st.caption("Upload your resume and paste a job description. This app calls your secure backend on Render.")

# ---------- Backend URL ----------
default_backend = st.secrets.get("BACKEND_URL", "")
backend_url = st.text_input(
    "Backend URL (from Render)",
    value=default_backend,
    placeholder="https://resume-ai-backend.onrender.com"
)
if not backend_url:
    st.info("Enter your backend URL (ending in .onrender.com).")

tone = st.selectbox("Cover letter tone", ["Professional", "Confident", "Friendly", "Persuasive"], index=0)

# ---------- Inputs ----------
c1, c2 = st.columns(2)
with c1:
    resume_file = st.file_uploader("Upload resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
with c2:
    job_text = st.text_area("Paste the job description", height=220)

def parse_resume(file) -> str:
    """Extract plain text from PDF/DOCX/TXT."""
    name = file.name.lower()
    data = file.read()
    if name.endswith(".pdf"):
        reader = PdfReader(BytesIO(data))
        parts = []
        for p in reader.pages:
            try:
                parts.append(p.extract_text() or "")
            except Exception:
                pass
        return "\n".join(parts)
    elif name.endswith(".docx"):
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return ""

if st.button("Generate", type="primary", use_container_width=True):
    if not backend_url:
        st.error("Please enter your Backend URL first.")
        st.stop()
    if not resume_file or not job_text.strip():
        st.error("Please upload a resume and paste the job description.")
        st.stop()

    with st.spinner("Reading resume..."):
        resume_text = parse_resume(resume_file)
        if not resume_text.strip():
            st.error("Could not read text from the resume. Try uploading a TXT or DOCX.")
            st.stop()

    payload = {
        "resume_text": resume_text,
        "job_text": job_text.strip(),
        "tone": tone
    }

    try:
        with st.spinner("Calling backend to generate your documents..."):
            r = requests.post(f"{backend_url.rstrip('/')}/generate", json=payload, timeout=90)
        if r.status_code != 200:
            st.error(f"Backend error ({r.status_code}): {r.text}")
            st.stop()
        data = r.json()
    except Exception as e:
        st.error(f"Request failed: {e}")
        st.stop()

    left, right = st.columns(2)
    with left:
        st.subheader("📄 Tailored Resume")
        st.text_area("Resume (editable)", value=data.get("tailored_resume", "").strip(), height=500, key="resume_out")
        st.download_button("⬇️ Download Resume (.txt)", data=st.session_state["resume_out"], file_name="resume_tailored.txt")

    with right:
        st.subheader("✉️ Cover Letter")
        st.text_area("Cover Letter (editable)", value=data.get("cover_letter", "").strip(), height=500, key="cl_out")
        st.download_button("⬇️ Download Cover Letter (.txt)", data=st.session_state["cl_out"], file_name="cover_letter.txt")

st.markdown("---")
st.caption("Tip: In Streamlit Cloud, set BACKEND_URL in Settings → Secrets so the textbox is pre-filled.")
