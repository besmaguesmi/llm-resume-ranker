import streamlit as st
import tempfile
import os
from app.resume_processor import ResumeProcessor
from app.matcher import ResumeMatcher
from app.ui import show_results

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("AI-Powered Resume Screener")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)", type=["pdf"], accept_multiple_files=True
)
job_description = st.text_area("Paste Job Description", height=200)

if st.button("Screen Resumes") and uploaded_files and job_description:
    processor = ResumeProcessor()
    temp_paths = []
    for f in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(f.read())
            temp_paths.append(tmp.name)
    with st.spinner("Processing resumes..."):
        processor.process_resumes(temp_paths)
    matcher = ResumeMatcher(processor.vector_store)
    show_results(matcher, job_description)
    for p in temp_paths:
        os.unlink(p)
