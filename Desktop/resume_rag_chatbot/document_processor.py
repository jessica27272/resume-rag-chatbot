import os
from typing import List
import PyPDF2
from docx import Document

class DocumentProcessor:
    def __init__(self, docs_folder: str = "documents"):
        self.docs_folder = docs_folder
        if not os.path.exists(docs_folder):
            os.makedirs(docs_folder)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        try:
            doc = Document(docx_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
            return ""
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT {txt_path}: {e}")
            return ""
    
    def process_all_documents(self) -> List[dict]:
        documents = []
        for filename in os.listdir(self.docs_folder):
            file_path = os.path.join(self.docs_folder, filename)
            text = ""
            if filename.endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
            elif filename.endswith('.docx'):
                text = self.extract_text_from_docx(file_path)
            elif filename.endswith('.txt'):
                text = self.extract_text_from_txt(file_path)
            if text.strip():
                documents.append({'filename': filename, 'content': text, 'source': file_path})
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks
