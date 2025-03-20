# data_ingestion/main.py
import os
import json
import logging
import fitz 
from pathlib import Path
from config import Config
import shutil

class DataIngestion:
    def __init__(self):
        self.config = Config()

    def process_pdf(self, pdf_path: Path, paper_id: str):
        try:
            paper_dir = self.config.PROCESSED_DIR / paper_id
            paper_dir.mkdir(parents=True, exist_ok=True)

            figures_dir = paper_dir / "figures"
            figures_dir.mkdir(exist_ok=True)

            doc = fitz.open(pdf_path)
            text = "\n".join([page.get_text() for page in doc])

            output_pdf_path = paper_dir / "fulltext.pdf"
            shutil.copy(pdf_path, output_pdf_path)
            
            figures = []
            for page_num, page in enumerate(doc):
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list):
                    pix = fitz.Pixmap(doc, img[0])
                    img_path = figures_dir / f"p{page_num}_fig{img_index}.png"
                    pix.save(img_path)
                    figures.append({
                        "path": str(img_path.relative_to(paper_dir)),
                        "page": page_num,
                        "caption": ""
                    })

            metadata = {
                "paper_id": paper_id,
                "title": doc.metadata.get("title", "Untitled"),
                "source_path": str(pdf_path)
            }

            output = {
                "metadata": metadata,
                "text": text,
                "figures": figures
            }
            
            with open(paper_dir / "raw_data.json", "w") as f:
                json.dump(output, f, indent=2)

            logging.info(f"Processed {paper_id} → {paper_dir}")
            return True

        except Exception as e:
            logging.error(f"Failed to process {pdf_path}: {str(e)}")
            return False

def process_all_pdfs():
    ingestor = DataIngestion()
    for pdf_file in Path(Config.PDF_DIR).glob("*.pdf"):
        paper_id = pdf_file.stem 
        ingestor.process_pdf(pdf_file, paper_id)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    Config.setup_dirs()
    process_all_pdfs()