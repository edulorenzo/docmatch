import docx

# Path to your test .docx file
file_path = 'cvs/cv3.docx'

try:
    doc = docx.Document(file_path)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    print(f"Extracted text from {file_path}:")
    print(text)
except Exception as e:
    print(f"Error reading {file_path}: {e}")
