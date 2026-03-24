# Triage App - Backend API

This repository contains the FastAPI backend for the Triage application, specifically addressing the scope for **Collaborator 3 (API & DB)**.

## Features Developed
- **FastAPI application** with dedicated routers.
- **SQLite Database Integration** using SQLAlchemy.
- **Data Models**: `Patient`, `TriageHistory`, and `Bed`.
- **Endpoints**:
  - `POST /patients/` - Admit a new patient.
  - `GET /patients/` - List patients.
  - `GET /patients/next` - Get the next patient based on their triage priority.
  - `PUT /patients/{id}` - Update a patient manually.
  - `POST /patients/{id}/assign-bed` - Assign a free bed to a patient.
  - `POST /triage/{patient_id}/reevaluate` - Update the triage level and log it.
  - `GET /triage/{patient_id}/history` - History of triage reevaluations.
- **Integration Tests** with `pytest`.

## Setup and Running

### 1. Requirements
Ensure you have Python 3.9+ installed. Install the dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application
Start the application using `uvicorn`:
```bash
# Make sure you are inside the backend folder
cd backend
python -m uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`. 
You can access the automated API documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### 3. Run Tests
To run the integration tests using `pytest` and the `TestClient`:
```bash
cd backend
python -m pytest tests/
```