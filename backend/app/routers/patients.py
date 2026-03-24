from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database.session import get_db
from app.services.patient_flow import PatientFlowManager

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

@router.post("/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    mgr = PatientFlowManager(db)
    return mgr.admit_patient(patient)

@router.get("/", response_model=List[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = crud.get_patients(db, skip=skip, limit=limit)
    return patients

@router.get("/next", response_model=schemas.Patient)
def get_next_patient(db: Session = Depends(get_db)):
    mgr = PatientFlowManager(db)
    patient = mgr.get_next_patient()
    if not patient:
        raise HTTPException(status_code=404, detail="No patients waiting for treatment")
    return patient

@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, status: schemas.PatientUpdate, db: Session = Depends(get_db)):
    if status.status:
        db_patient = crud.update_patient_status(db, patient_id=patient_id, status=status.status)
        if not db_patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return db_patient
    
    db_patient = crud.get_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.post("/{patient_id}/assign-bed", response_model=schemas.Bed)
def assign_bed(patient_id: int, db: Session = Depends(get_db)):
    mgr = PatientFlowManager(db)
    try:
        bed = mgr.assign_bed(patient_id=patient_id)
        return bed
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
