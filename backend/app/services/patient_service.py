from collections import deque
from .triage_service import infer_triage_level
from ..models import TriageLevel as TriageStatus

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


class PatientFlowManager:
    def __init__(self, bed_capacity: int = 10):
        self.waiting_queue = deque()  # Cola para Admision
        self.urgent_stack = []  # Pila para Reevaluacion
        self.beds = [None] * bed_capacity # Lista de camas

    def admit_patient(self, name: str, age: int, symptoms: str) -> Patient:
        patient = Patient(name=name, age=age)
        patient.assign_triage_level(symptoms)
        self.waiting_queue.append(patient)
        return patient

    def next_patient(self) -> Patient | None:
        if self.urgent_stack:
            return self.urgent_stack.pop()

        if self.waiting_queue:
            return self.waiting_queue.popleft()

        return None

    def mark_for_reevaluation(self, patient: Patient):
        patient.status = "reevaluation"
        self.urgent_stack.append(patient)

    def assign_bed(self, patient: Patient) -> int:
        for i in range(len(self.beds)):
            if self.beds[i] is None:
                self.beds[i] = patient.id
                patient.status = "in_treatment"
                return i
        raise RuntimeError("No hay camas disponibles")

    def release_bed(self, index: int):
        if 0 <= index < len(self.beds) and self.beds[index] is not None:
            self.beds[index] = None
        else:
            raise ValueError("Index de cama invalido o cama ya libre")

    def get_bed_status(self) -> list:
        return list(self.beds)
