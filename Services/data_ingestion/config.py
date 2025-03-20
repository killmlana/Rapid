import os
from dotenv import load_dotenv
from pathlib import Path
import logging

load_dotenv()

class Config:
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Input/Output paths
    PDF_DIR = DATA_DIR / "raw_pdfs"
    PROCESSED_DIR = DATA_DIR / "processed"
    
    @classmethod
    def setup_dirs(cls):
        try:
            cls.PDF_DIR.mkdir(parents=True, exist_ok=True)
            cls.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
            os.chmod(cls.PROCESSED_DIR, 0o755)  # Read/write/search for all users
        except PermissionError:
            raise RuntimeError(f"Permission denied for {cls.PROCESSED_DIR}")

    @classmethod
    def verify_paths(cls):
        print(f"Current working directory: {os.getcwd()}")
        print(f"BASE_DIR exists: {cls.BASE_DIR.exists()}")
        print(f"PDF_DIR: {cls.PDF_DIR} (exists: {cls.PDF_DIR.exists()})")
        print(f"OUTPUT_DIR: {cls.OUTPUT_DIR} (exists: {cls.OUTPUT_DIR.exists()})")
    
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
    
    GROBID_URL = os.getenv("GROBID_URL", "http://localhost:8070/api/processFulltextDocument")