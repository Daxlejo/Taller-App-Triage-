from sqlalchemy.orm import Session
from app import crud

class PatientFlowManager:
    """
    Service class that handles complex flows relying on the DB.
    """
    def __init__(self, db: Session):
        self.db = db
        
    def admit_patient(self, patient_data):
        return crud.create_patient(self.db, patient_data)

    def get_next_patient(self):
        return crud.get_next_patient_for_treatment(self.db)

    def assign_bed(self, patient_id: int):
        target_bed = crud.get_available_bed(self.db)
        if not target_bed:
            raise Exception("No beds available")
            
        assigned_bed = crud.assign_bed_to_patient(self.db, patient_id=patient_id, bed_id=target_bed.id)
        if not assigned_bed:
            raise Exception("Could not assign bed (patient might not exist or bed is occupied)")
            
        return assigned_bed
