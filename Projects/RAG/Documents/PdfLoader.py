from PyPDF2 import PdfReader
from utils.Document import Document

class LoadPDF:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        documents = []
        with open(self.file_path, "rb") as f:
            reader = PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                documents.append(Document(
                    page_content=text,
                    metadata={"source": self.file_path, "page": i + 1}
                ))
        print(documents[0])
        return documents
    
    