# Streamlit Frontend for AI Resume & Cover Letter Generator

This is a simple Streamlit web app that:
- Uploads your resume (PDF/DOCX/TXT)
- Accepts a job description
- Calls your FastAPI backend on Render to generate:
  - Tailored Resume
  - Custom Cover Letter

## Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
