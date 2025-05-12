# utils.py
import os
import pdfplumber
import docx
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif ext == '.pdf':
        try:
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)
        except:
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

def calculate_match(cv_text, jd_text):
    if not cv_text.strip() or not jd_text.strip():
        return 0.0

    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(cv_embedding, jd_embedding).item()
    return similarity * 100


def compute_similarity(doc1, doc2):
    embeddings = model.encode([doc1, doc2], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity[0][0]) * 100, 2)