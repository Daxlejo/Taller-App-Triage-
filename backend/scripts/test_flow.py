import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # sube de scripts/ a App/
sys.path.insert(0, str(ROOT))

from backend.app.services.patient_service import PatientFlowManager
from backend.app.models import TriageLevel

m = PatientFlowManager(bed_capacity=2)
p = m.admit_patient("Ana", 32, "dolor pecho y dificultad respiratoria severa")
print(p.name, p.triage_level, p.assigned_by, p.triage_history)
print("queue", len(m.waiting_queue), "beds", m.get_bed_status())
np = m.next_patient()
b = m.assign_bed(np)
print("Next", np.name, "bed", b, m.get_bed_status())