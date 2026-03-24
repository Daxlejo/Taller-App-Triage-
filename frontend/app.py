import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Triage App", layout="wide")

def admit_patient():
    st.header("Admit a Patient")
    with st.form("admission_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        symptoms = st.text_area("Symptoms")
        submitted = st.form_submit_button("Admit")

        if submitted:
            if not name or not symptoms:
                st.error("Name and symptoms are required.")
            else:
                payload = {"name": name, "age": age, "symptoms": symptoms}
                try:
                    response = requests.post(f"{API_URL}/patients/", json=payload)
                    if response.status_code == 200:
                        st.success(f"Patient {name} admitted successfully!")
                    else:
                        st.error(f"Error admitting patient: {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to backend server. Make sure FastAPI is running.")

def view_patients():
    st.header("Patient List")
    try:
        response = requests.get(f"{API_URL}/patients/")
        if response.status_code == 200:
            patients = response.json()
            if patients:
                df = pd.DataFrame(patients)
                # Keep only relevant columns
                display_df = df[["id", "name", "age", "status", "triage_level", "assigned_by", "created_at"]]
                st.dataframe(display_df, use_container_width=True)
                
                st.subheader("Manage Patient")
                col1, col2 = st.columns(2)
                
                # Assign Bed feature
                with col1:
                    patient_id_bed = st.number_input("Patient ID to assign bed", min_value=1, step=1)
                    if st.button("Assign Bed"):
                        res = requests.post(f"{API_URL}/patients/{patient_id_bed}/assign-bed")
                        if res.status_code == 200:
                            st.success(f"Bed assigned successfully to Patient {patient_id_bed}")
                        else:
                            st.error(f"Failed to assign bed: {res.text}")
                
                # Reevaluate Triage feature
                with col2:
                    patient_id_triage = st.number_input("Patient ID to reevaluate", min_value=1, step=1)
                    new_level = st.selectbox("New Level", ["Red", "Orange", "Yellow", "Green", "Blue", "Unassigned"])
                    doctor_name = st.text_input("Evaluated by")
                    notes = st.text_input("Notes")
                    if st.button("Reevaluate Triage"):
                        if not doctor_name:
                            st.error("Evaluator name is required.")
                        else:
                            payload = {"new_level": new_level, "evaluated_by": doctor_name, "notes": notes}
                            res = requests.post(f"{API_URL}/triage/{patient_id_triage}/reevaluate", json=payload)
                            if res.status_code == 200:
                                st.success("Triage updated!")
                            else:
                                st.error(f"Failed to update triage: {res.text}")
                
            else:
                st.info("No patients currently in the system.")
        else:
            st.error(f"Failed to fetch patients. State: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to backend server. Make sure FastAPI is running.")

def dashboard():
    st.header("Dashboard")
    try:
        # Fetch patients
        response = requests.get(f"{API_URL}/patients/")
        if response.status_code == 200:
            patients = response.json()
            
            # Simple metrics
            total_patients = len(patients)
            triaged = sum(1 for p in patients if p['status'] == 'Triaged')
            waiting = sum(1 for p in patients if p['status'] == 'Waiting Triage')
            in_treatment = sum(1 for p in patients if p['status'] == 'In Treatment')
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Patients", total_patients)
            col2.metric("Waiting Triage", waiting)
            col3.metric("Triaged (Waiting Bed)", triaged)
            col4.metric("In Treatment", in_treatment)
            
            # Show next patient
            st.subheader("Next Patient waiting for Treatment")
            next_res = requests.get(f"{API_URL}/patients/next")
            if next_res.status_code == 200:
                nxt = next_res.json()
                st.info(f"ID: {nxt['id']} | Name: {nxt['name']} | Level: {nxt['triage_level']} | Symptoms: {nxt['symptoms']}")
            else:
                st.warning("No patients currently waiting for treatment (Triaged stage).")
                
        else:
            st.error(f"Failed to fetch stats. State: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to backend server.")

def main():
    st.sidebar.title("Triage App Menu")
    menu = ["Admit Patient", "Patient List", "Dashboard"]
    choice = st.sidebar.radio("Navigate", menu)

    if choice == "Admit Patient":
        admit_patient()
    elif choice == "Patient List":
        view_patients()
    elif choice == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
