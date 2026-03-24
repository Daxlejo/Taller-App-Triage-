from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models import TriageLevel, PatientStatus

class TriageHistoryBase(BaseModel):
    previous_level: TriageLevel
    new_level: TriageLevel
    evaluated_by: str
    notes: Optional[str] = None

class TriageHistoryCreate(TriageHistoryBase):
    pass

class TriageHistory(TriageHistoryBase):
    id: int
    patient_id: int
    evaluation_time: datetime

    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    age: int
    symptoms: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    symptoms: Optional[str] = None
    status: Optional[PatientStatus] = None
    triage_level: Optional[TriageLevel] = None
    assigned_by: Optional[str] = None

class TriageReevaluation(BaseModel):
    new_level: TriageLevel
    evaluated_by: str
    notes: Optional[str] = None

class BedBase(BaseModel):
    name: str

class BedCreate(BedBase):
    pass

class Bed(BedBase):
    id: int
    is_occupied: bool
    patient_id: Optional[int] = None

    class Config:
        from_attributes = True

class Patient(PatientBase):
    id: int
    status: PatientStatus
    triage_level: TriageLevel
    assigned_by: Optional[str] = None
    created_at: datetime
    triage_history: List[TriageHistory] = []
    bed: Optional[Bed] = None

    class Config:
        orm_mode = True
        