from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database.session import get_db

router = APIRouter(
    prefix="/triage",
    tags=["triage"]
)

@router.post("/{patient_id}/reevaluate", response_model=schemas.Patient)
def reevaluate_patient(
    patient_id: int, 
    reeval: schemas.TriageReevaluation, 
    db: Session = Depends(get_db)
):
    patient = crud.update_patient_triage(
        db, 
        patient_id=patient_id, 
        new_level=reeval.new_level,
        evaluated_by=reeval.evaluated_by,
        notes=reeval.notes
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/{patient_id}/history", response_model=List[schemas.TriageHistory])
def get_triage_history(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient.triage_history
