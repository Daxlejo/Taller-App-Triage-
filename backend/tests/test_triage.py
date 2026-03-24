def test_reevaluate_triage_and_history(client):
    # Admit patient
    resp = client.post("/patients/", json={"name": "Alice", "age": 40, "symptoms": "cefalea"})
    p_id = resp.json()["id"]

    # Check initial triage (GREEN for cefalea)
    assert resp.json()["triage_level"] == "Green"

    # Reevaluate 1
    resp_t1 = client.post(f"/triage/{p_id}/reevaluate", json={"new_level": "Yellow", "evaluated_by": "Nurse Joy", "notes": "Initial assessment"})
    assert resp_t1.status_code == 200
    assert resp_t1.json()["triage_level"] == "Yellow"

    # Reevaluate 2
    resp_t2 = client.post(f"/triage/{p_id}/reevaluate", json={"new_level": "Orange", "evaluated_by": "Dr. House", "notes": "Condition worsened"})
    assert resp_t2.status_code == 200
    assert resp_t2.json()["triage_level"] == "Orange"

    # Get History
    hist_resp = client.get(f"/triage/{p_id}/history")
    assert hist_resp.status_code == 200
    history_data = hist_resp.json()

    assert len(history_data) == 3  # initial + 2 reevaluations
    assert history_data[0]["previous_level"] == "Unassigned"
    assert history_data[0]["new_level"] == "Green"
    assert history_data[1]["previous_level"] == "Green"
    assert history_data[1]["new_level"] == "Yellow"
    assert history_data[2]["previous_level"] == "Yellow"
    assert history_data[2]["new_level"] == "Orange"
    assert history_data[2]["evaluated_by"] == "Dr. House"
