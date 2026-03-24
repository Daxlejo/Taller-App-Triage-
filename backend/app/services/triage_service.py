from ..models.triage import TriageStatus
from ..utils.triage_rules import TRIAGE_SYMPTOMS

def infer_triage_level(symptoms_text: str) -> TriageStatus:
    txt = symptoms_text.lower()
    for level, keywords in TRIAGE_SYMPTOMS.items():
        for kw in keywords:
            if kw in txt:
                return level
    return TriageStatus.BLUE