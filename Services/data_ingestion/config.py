import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PDF_DIR = "data/raw_pdfs"
    OUTPUT_DIR = "data/processed"
    FIGURE_DIR = os.path.join(OUTPUT_DIR, "figures")
    
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
    
    GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070/api/processFulltextDocument")