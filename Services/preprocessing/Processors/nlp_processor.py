
import spacy
from transformers import pipeline
from typing import List, Dict

class ScientificNLP:
    def __init__(self):
        self.ner = spacy.load('en_core_sci_scibert')
        self.claim_detector = pipeline(
            "text-classification"
        )
        self.relation_model = None  # Could add SciBERT-based relation extraction

    def analyze_text(self, text: str) -> Dict:
        doc = self.ner(text)
        
        return {
            "entities": [
                {"text": ent.text, "label": ent.label_, "start": ent.start_char}
                for ent in doc.ents
            ],
            "claims": self._detect_claims(text),
            "relations": self._extract_relations(doc)
        }

    def _detect_claims(self, text: str) -> List[Dict]:
        return self.claim_detector(text, top_k=3, truncation=True)

    def _extract_relations(self, doc) -> List[Dict]:
        return [
            {"source": ent1.text, "target": ent2.text, "type": "co-occurrence"}
            for ent1 in doc.ents 
            for ent2 in doc.ents 
            if ent1 != ent2 and ent1.sent == ent2.sent
        ]