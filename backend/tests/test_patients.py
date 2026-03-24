def test_admit_patient(client):
    response = client.post(
        "/patients/",
        json={"name": "John Doe", "age": 30, "symptoms": "dolor torácico intenso"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["status"] == "Triaged"
    assert data["triage_level"] == "Orange"
    assert "id" in data

def test_get_next_patient_no_triage(client):
    # Admit but triage is automatic, so status Triaged
    client.post("/patients/", json={"name": "John Doe", "age": 30, "symptoms": "dolor leve"})
    
    response = client.get("/patients/next")
    # It should return the patient
    assert response.status_code == 200

def test_triage_and_get_next(client):
    # Admit patient 1
    resp1 = client.post("/patients/", json={"name": "P1", "age": 20, "symptoms": "tos"})
    p1_id = resp1.json()["id"]

    # Admit patient 2
    resp2 = client.post("/patients/", json={"name": "P2", "age": 25, "symptoms": "hemorragia masiva"})
    p2_id = resp2.json()["id"]

    # P1 is GREEN (tos), P2 is RED (hemorragia)
    # Get Next -> should be P2 because RED is higher priority than GREEN
    response = client.get("/patients/next")
    assert response.status_code == 200
    assert response.json()["id"] == p2_id

def test_assign_bed(client):
    # Admit and triage
    resp = client.post("/patients/", json={"name": "P1", "age": 20, "symptoms": "Cough"})
    p_id = resp.json()["id"]
    client.post(f"/triage/{p_id}/reevaluate", json={"new_level": "Green", "evaluated_by": "Dr. Smith"})

    # Assign bed automatic
    resp = client.post("/patients/", json={"name": "P1", "age": 20, "symptoms": "Cough"})
    p_id = resp.json()["id"]
    assert data["is_occupied"] == True
    assert data["patient_id"] == p_id

    # Check patient status changed to In Treatment
    p_resp = client.get("/patients/?limit=10")
    patient_data = next((p for p in p_resp.json() if p["id"] == p_id), None)
    assert patient_data is not None
    assert patient_data["status"] == "In Treatment"
