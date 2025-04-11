# main.py
from gui import launch_gui

if __name__ == '__main__':
    launch_gui()


# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from resume_parser import extract_text_from_file
from matcher import calculate_match_score


def launch_gui():
    def upload_resume():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
        resume_path.set(file_path)

    def check_match():
        resume_file = resume_path.get()
        job_text = job_desc.get("1.0", tk.END)

        if not resume_file or not job_text.strip():
            messagebox.showerror("Error", "Please upload a resume and paste a job description.")
            return

        resume_text = extract_text_from_file(resume_file)
        match_score = calculate_match_score(resume_text, job_text)
        result_var.set(f"Match Score: {match_score:.2f}%")

    root = tk.Tk()
    root.title("Resume ATS Checker")
    root.geometry("600x500")

    resume_path = tk.StringVar()
    result_var = tk.StringVar()

    tk.Label(root, text="1. Upload Resume (PDF or DOCX)").pack(pady=5)
    tk.Button(root, text="Choose File", command=upload_resume).pack(pady=5)
    tk.Label(root, textvariable=resume_path).pack(pady=5)

    tk.Label(root, text="2. Paste Job Description").pack(pady=5)
    job_desc = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
    job_desc.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    tk.Button(root, text="Check Match", command=check_match).pack(pady=10)
    tk.Label(root, textvariable=result_var, font=("Arial", 14)).pack(pady=10)

    root.mainloop()


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


# matcher.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_desc):
    docs = [resume_text, job_desc]
    tfidf = TfidfVectorizer().fit_transform(docs)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return score * 100  # Convert to percentage
