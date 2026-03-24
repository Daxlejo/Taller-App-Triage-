from .triage_service import infer_triage_level

class Patient:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.triage_level = None
        self.status = "waiting"
        self.assigned_by = None
        self.triage_history = []
        self.id = None

    def assign_triage_level(self, symptoms: str):
        self.triage_level = infer_triage_level(symptoms)
        self.status = "triaged"
        self.assigned_by = "Automatic"
        self.triage_history.append({"level": self.triage_level, "evaluated_by": "Automatic", "time": "now"})