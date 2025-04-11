# resume_parser.py
import fitz  # PyMuPDF
import docx

def extract_text_from_file(filepath):
    if filepath.endswith(".pdf"):
        text = ""
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
        return text
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""
