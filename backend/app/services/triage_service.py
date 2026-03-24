import unicodedata
from ..models import TriageLevel
from ..utils.triage_rules import TRIAGE_SYMPTOMS

def infer_triage_level(symptoms_text: str) -> TriageLevel:
    txt = unicodedata.normalize('NFD', symptoms_text.lower()).encode('ascii', 'ignore').decode('ascii')
    for level, keywords in TRIAGE_SYMPTOMS.items():
        for kw in keywords:
            if kw in txt:
                return level
    return TriageLevel.BLUE