from sqlalchemy.orm import Session
from app import models, schemas
from app.models import TriageLevel
from app.services.triage_service import infer_triage_level

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(
        name=patient.name,
        age=patient.age,
        symptoms=patient.symptoms
    )
    triage_level = infer_triage_level(patient.symptoms)
    db_patient.triage_level = triage_level
    db_patient.assigned_by = "Automatic"
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    # Create initial triage history
    history = models.TriageHistory(
        patient_id=db_patient.id,
        previous_level=models.TriageLevel.UNASSIGNED,
        new_level=triage_level,
        evaluated_by="Automatic"
    )
    db.add(history)
    db.commit()
    return db_patient

def update_patient_status(db: Session, patient_id: int, status: models.PatientStatus):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db_patient.status = status
        db.commit()
        db.refresh(db_patient)
    return db_patient

def update_patient_triage(db: Session, patient_id: int, new_level: TriageLevel, evaluated_by: str, notes: str = None):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None

    history = models.TriageHistory(
        patient_id=patient_id,
        previous_level=db_patient.triage_level,
        new_level=new_level,
        evaluated_by=evaluated_by,
        notes=notes
    )
    db.add(history)

    db_patient.triage_level = new_level
    db_patient.assigned_by = evaluated_by
    if db_patient.status == models.PatientStatus.WAITING_TRIAGE:
        db_patient.status = models.PatientStatus.TRIAGED

    db.commit()
    db.refresh(db_patient)
    return db_patient

def create_bed(db: Session, bed: schemas.BedCreate):
    db_bed = models.Bed(name=bed.name)
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed

def get_beds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bed).offset(skip).limit(limit).all()

def get_available_bed(db: Session):
    return db.query(models.Bed).filter(models.Bed.is_occupied == False).first()

def assign_bed_to_patient(db: Session, patient_id: int, bed_id: int):
    db_bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()
    db_patient = get_patient(db, patient_id)

    if db_bed and db_patient and not db_bed.is_occupied:
        db_bed.is_occupied = True
        db_bed.patient_id = patient_id
        
        db_patient.status = models.PatientStatus.IN_TREATMENT
        
        db.commit()
        db.refresh(db_bed)
        db.refresh(db_patient)
        return db_bed
    return None

def get_next_patient_for_treatment(db: Session):
    priority_order = {
        TriageLevel.RED: 1,
        TriageLevel.ORANGE: 2,
        TriageLevel.YELLOW: 3,
        TriageLevel.GREEN: 4,
        TriageLevel.BLUE: 5,
        TriageLevel.UNASSIGNED: 6
    }
    
    patients = db.query(models.Patient).filter(
        models.Patient.status == models.PatientStatus.TRIAGED
    ).all()

    if not patients:
         return None
         
    patients.sort(key=lambda p: (priority_order.get(p.triage_level, 6), p.created_at))
    return patients[0]
