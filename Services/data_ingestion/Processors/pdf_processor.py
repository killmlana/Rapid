import fitz  
import os
from tqdm import tqdm
from config import Config
import logging

class PDFProcessor:
    def __init__(self):
        self.config = Config()
        os.makedirs(self.config.FIGURE_DIR, exist_ok=True)

    def _extract_text(self, doc):
        text = ""
        for page in doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                if block[6] == 0:
                    text += block[4] + "\n"
        return text.strip()

    def _extract_figures(self, doc, paper_id):
        figure_data = []
        for page_num, page in enumerate(doc):
            images = page.get_images()
            for img_index, img in enumerate(images):
                pix = fitz.Pixmap(doc, img[0])
                img_path = os.path.join(
                    self.config.FIGURE_DIR, 
                    f"{paper_id}_p{page_num}_fig{img_index}.png"
                )
                pix.save(img_path)
                figure_data.append({
                    "path": img_path,
                    "page": page_num,
                    "caption": ""
                })
        return figure_data

    def process_pdf(self, pdf_path, paper_id):
        try:
            doc = fitz.open(pdf_path)
            text = self._extract_text(doc)
            figures = self._extract_figures(doc, paper_id)
            return {
                "text": text,
                "figures": figures,
                "paper_id": paper_id
            }
        except Exception as e:
            logging.error(f"Error processing {pdf_path}: {str(e)}")
            return None