from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routers import patients, triage
from app.database.session import SessionLocal
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Triage App API",
    description="API for Triage and Patient Flow management",
    version="1.0.0"
)

app.include_router(patients.router)
app.include_router(triage.router)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        if not crud.get_beds(db):
            for i in range(1, 6):
                crud.create_bed(db, schemas.BedCreate(name=f"Bed {i}"))
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Triage App"}
