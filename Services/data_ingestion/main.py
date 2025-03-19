import os
from config import Config
from Processors.pdf_processor import PDFProcessor
from Processors.ocr_processor import OCRProcessor
from Processors.metadata import MetadataExtractor
import json
import logging

def process_all_pdfs():
    config = Config()
    pdf_processor = PDFProcessor()
    ocr_processor = OCRProcessor()
    metadata_extractor = MetadataExtractor(use_grobid=False)
    
    for pdf_file in os.listdir(config.PDF_DIR):
        if not pdf_file.endswith(".pdf"):
            continue
        
        pdf_path = os.path.join(config.PDF_DIR, pdf_file)
        paper_id = os.path.splitext(pdf_file)[0]
        
        paper_data = pdf_processor.process_pdf(pdf_path, paper_id)
        if not paper_data:
            continue
        
        for fig in paper_data["figures"]:
            fig["ocr_text"] = ocr_processor.extract_text_from_image(fig["path"])
        
        paper_data["metadata"] = metadata_extractor.extract_basic_metadata(pdf_path)
        
        output_path = os.path.join(config.OUTPUT_DIR, f"{paper_id}.json")
        with open(output_path, "w") as f:
            json.dump(paper_data, f, indent=2)
        
        logging.info(f"Processed {pdf_file} → {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    process_all_pdfs()