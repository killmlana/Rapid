# processors/figure_processor.py
from typing import Dict, List
import pytesseract
from PIL import Image
from pathlib import Path
import logging
import re

class FigureProcessor:
    def __init__(self):
        self.caption_pattern = re.compile(
            r'(?:Figure|Fig\.?)\s*(\d+)[:\.]?\s*(.*?)(?=\n\n|$)',
            re.DOTALL | re.IGNORECASE
        )

    def process_figures(self, figures_dir: Path, text: str) -> List[Dict]:
        try:
            figure_map = self._map_figures(text)
            processed = []
            
            for fig_path in figures_dir.glob("*.png"):
                fig_num = self._extract_figure_number(fig_path.name)
                processed.append({
                    "path": str(fig_path),
                    "number": fig_num,
                    "caption": figure_map.get(fig_num, ""),
                    "ocr_text": self._extract_ocr(fig_path),
                    "type": self._classify_figure(fig_path)
                })
            
            return processed
            
        except Exception as e:
            logging.error(f"Figure processing failed: {str(e)}")

    def _map_figures(self, text: str) -> Dict[int, str]:
        return {int(m.group(1)): m.group(2).strip() 
                for m in self.caption_pattern.finditer(text)}
    
    def _classify_figure(self, img_path: Path) -> str:
        """Classify using OCR text + visual features"""
        ocr_text = self._extract_ocr(img_path).lower()
        
        if any(x in ocr_text for x in ["table", "row", "column"]):
            return "table"
        elif any(x in ocr_text for x in ["graph", "plot", "axis"]):
            return "graph"
        return "diagram"