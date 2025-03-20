# config.py
from pathlib import Path
import logging

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PROCESSED_DIR = BASE_DIR / "data/processed"
    RAW_DIR = BASE_DIR / "data/raw_pdfs"
    LOG_DIR = BASE_DIR / "logs"
    SECTION_PATTERNS = {
        "abstract": {"keywords": ["abstract", "summary"], "priority": 1},
        "methods": {"keywords": ["method", "experiment", "protocol"], "priority": 2},
        "results": {"keywords": ["result", "finding", "observation"], "priority": 3},
        "discussion": {"keywords": ["discuss", "interpret", "analysis"], "priority": 4}
    }

    @classmethod
    def setup(cls):
        cls.PROCESSED_DIR.mkdir(exist_ok=True, parents=True)
        cls.LOG_DIR.mkdir(exist_ok=True)
        logging.basicConfig(
            filename=cls.LOG_DIR/'preprocessing.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

# exceptions.py
class PreprocessingError(Exception):
    """Base class for preprocessing exceptions"""
    
class SectionDetectionError(PreprocessingError):
    """Failed to detect document sections"""

class FigureProcessingError(PreprocessingError):
    """Error in figure processing pipeline"""