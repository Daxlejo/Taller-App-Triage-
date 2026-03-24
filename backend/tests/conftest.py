import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.connection import Base
from app.database.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_triage.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Setup
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Teardown
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    # Clean up test database between tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # create default beds
    db = TestingSessionLocal()
    from app import crud, schemas
    for i in range(1, 6):
        crud.create_bed(db, schemas.BedCreate(name=f"Bed {i}"))
    db.close()
