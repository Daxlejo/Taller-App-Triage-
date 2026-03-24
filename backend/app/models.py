import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database.connection import Base

class TriageLevel(str, enum.Enum):
    RED = "Red"
    ORANGE = "Orange"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    UNASSIGNED = "Unassigned"

class PatientStatus(str, enum.Enum):
    WAITING_TRIAGE = "Waiting Triage"
    TRIAGED = "Triaged"
    IN_TREATMENT = "In Treatment"
    DISCHARGED = "Discharged"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    symptoms = Column(String)
    status = Column(Enum(PatientStatus), default=PatientStatus.WAITING_TRIAGE)
    triage_level = Column(Enum(TriageLevel), default=TriageLevel.UNASSIGNED)
    assigned_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    triage_history = relationship("TriageHistory", back_populates="patient", cascade="all, delete-orphan")
    bed = relationship("Bed", back_populates="patient", uselist=False)

class TriageHistory(Base):
    __tablename__ = "triage_history"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    previous_level = Column(Enum(TriageLevel))
    new_level = Column(Enum(TriageLevel))
    evaluated_by = Column(String)
    evaluation_time = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="triage_history")

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_occupied = Column(Boolean, default=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)

    patient = relationship("Patient", back_populates="bed")
