import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
import os

def parse_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def build_syllabus_index(file_path):
    syllabus_text = parse_pdf(file_path)
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform([syllabus_text])
    return vectorizer, X, syllabus_text
