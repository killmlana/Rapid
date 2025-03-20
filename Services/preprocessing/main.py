# main.py
import json
import logging
from pathlib import Path
from config import Config
from Processors.text_processor import TextProcessor
from Processors.figure_processor import FigureProcessor
from Processors.nlp_processor import ScientificNLP
from Processors.postprocessor import QualityChecker

class PreprocessingPipeline:
    def __init__(self):
        Config.setup()
        self.text_processor = TextProcessor()
        self.figure_processor = FigureProcessor()
        self.nlp_processor = ScientificNLP()
        self.post_processor = QualityChecker()

    def process_paper(self, paper_dir: Path):
        try:
            with open(paper_dir / "raw_data.json") as f:
                raw_data = json.load(f)
            
            pdf_path = paper_dir / "fulltext.pdf"
            processed = {
                "metadata": raw_data["metadata"],
                "sections": self.text_processor.split_sections(
                    raw_data["text"], 
                    pdf_path
                ),
                "figures": self.figure_processor.process_figures(
                    paper_dir / "figures",
                    raw_data["text"]
                ),
                "nlp_analysis": self.nlp_processor.analyze_text(raw_data["text"])
            }
            
            # Quality checks
            #processed = self.quality_checker.validate_output(processed)
            
            with open(paper_dir / "processed.json", "w") as f:
                json.dump(processed, f, indent=2)
                
            return True
            
        except Exception as e:
            logging.error(f"Failed {paper_dir.name}: {str(e)}")

if __name__ == "__main__":
    pipeline = PreprocessingPipeline()
    
    for paper_dir in Config.PROCESSED_DIR.iterdir():
        if paper_dir.is_dir() and (paper_dir / "raw_data.json").exists():
            pipeline.process_paper(paper_dir)
            logging.info(f"Success: {paper_dir.name}")
            