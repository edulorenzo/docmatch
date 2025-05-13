# utils.py
import os
import docx
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match(cv_text, jd_text):
    if not cv_text.strip() or not jd_text.strip():
        return 0.0

    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(cv_embedding, jd_embedding).item()
    return similarity * 100

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif ext == '.pdf':
        try:
            return extract_text_from_pdf(file_path)
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            return ""

    elif ext == '.docx':
        try:
            doc = docx.Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            print(f"Error processing DOCX {file_path}: {e}")
            return ""

    else:
        print(f"Skipping unsupported file format: {file_path}")
        return ""
