import streamlit as st
from utils import load_text, calculate_match
import os

st.title("Document Matcher Web App")

jd_file = st.file_uploader("Upload Document Template", type=["txt", "pdf", "docx"])
cv_files = st.file_uploader("Upload Submission files", type=["txt", "pdf", "docx"], accept_multiple_files=True)

if st.button("Compare") and jd_file and cv_files:
    jd_path = f"temp_{jd_file.name}"
    with open(jd_path, "wb") as f:
        f.write(jd_file.read())
    jd_text = load_text(jd_path)
    os.remove(jd_path)

    for cv_file in cv_files:
        cv_path = f"temp_{cv_file.name}"
        with open(cv_path, "wb") as f:
            f.write(cv_file.read())
        cv_text = load_text(cv_path)
        score = calculate_match(cv_text, jd_text)
        st.write(f"**{cv_file.name}** → Match Score: {score:.2f}%")
        os.remove(cv_path)