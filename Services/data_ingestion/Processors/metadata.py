import fitz
import requests
from config import Config

class MetadataExtractor:
    def __init__(self, use_grobid=False):
        self.config = Config()
        self.use_grobid = use_grobid

    def extract_basic_metadata(self, pdf_path):
        doc = fitz.open(pdf_path)
        return {
            "title": doc.metadata.get("title", ""),
            "authors": doc.metadata.get("author", ""),
            "pages": len(doc)
        }

    def extract_grobid_metadata(self, pdf_path):
        with open(pdf_path, "rb") as f:
            files = {"input": f}
            response = requests.post(
                self.config.GROBID_URL,
                files=files,
                timeout=60
            )
        if response.status_code == 200:
            return self._parse_grobid_xml(response.text)
        else:
            return {}

    def _parse_grobid_xml(self, xml_text):
        return {
            "title": "TODO: Extract from XML",
            "authors": [],
            "references": []
        }