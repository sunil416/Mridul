
from datetime import datetime
from utils.Document import Document
class TextLoader:
    def __init__(self, filepath, encoding="utf-8"):
        self.filepath = filepath
        self.encoding = encoding

    def load(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            content = f.read()

        metadata = {
            "source": self.filepath,
            "length": len(content),
            "loaded_at": datetime.now().isoformat()
        }

        return [Document(page_content=content, metadata=metadata)]
