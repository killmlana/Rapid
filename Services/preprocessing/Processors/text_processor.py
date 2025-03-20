# processors/text_processor.py
from pathlib import Path
import re
import fitz
from typing import Dict, List
from config import Config
import logging

class TextProcessor:
    def __init__(self):
        self.section_rules = self._compile_rules()
        
    def _compile_rules(self):
        rules = []
        for section, config in Config.SECTION_PATTERNS.items():
            pattern = re.compile(
                r'^.*?\b(' + 
                '|'.join(config["keywords"]) + 
                r')\b.*$', 
                re.IGNORECASE
            )
            rules.append((pattern, section, config["priority"]))
        return sorted(rules, key=lambda x: x[2], reverse=True)

    def _classify_section(self, text: str) -> str:
        for pattern, section, _ in self.section_rules:
            if pattern.search(text):
                return section
        return "other"  

    def _detect_via_formatting(self, doc: fitz.Document) -> Dict[str, List[str]]:
        sections = {}
        current_section = "header"
        
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["size"] > 12 and span["flags"] & 2**4:  
                                section = self._classify_section(span["text"])
                                if section != current_section:
                                    current_section = section
                                    sections[current_section] = []
                        sections[current_section].append(line["text"])
        return {k: "\n".join(v) for k, v in sections.items()}

    def split_sections(self, text: str, pdf_path: Path) -> Dict[str, str]:
        try:
            doc = fitz.open(pdf_path)
            return self._detect_via_formatting(doc)
        except Exception as e:
            logging.error(f"Section detection failed: {str(e)}")
            return {"full_text": text} 