import pytesseract
from PIL import Image
from config import Config
import logging

class OCRProcessor:
    def __init__(self):
        self.config = Config()
        pytesseract.pytesseract.tesseract_cmd = self.config.TESSERACT_CMD

    def extract_text_from_image(self, image_path):
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            logging.error(f"OCR failed for {image_path}: {str(e)}")
            return ""