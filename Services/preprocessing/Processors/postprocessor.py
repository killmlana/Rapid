
from typing import Dict

class QualityChecker:
    VALID_SECTIONS = ["abstract", "methods", "results", "discussion"]
    
    def validate_output(self, processed_data: Dict) -> Dict:
        validation = {
            "missing_sections": [],
            "figure_issues": [],
            "entity_coverage": 0.0
        }
        

        for section in self.VALID_SECTIONS:
            if section not in processed_data["sections"]:
                validation["missing_sections"].append(section)
        

        for fig in processed_data.get("figures", []):
            if not fig["caption"] and not fig["ocr_text"]:
                validation["figure_issues"].append(f"Figure {fig['number']}")
        

        total_entities = len(processed_data.get("entities", []))
        validation["entity_coverage"] = min(total_entities / 100, 1.0) 
        
        return {**processed_data, "validation": validation}