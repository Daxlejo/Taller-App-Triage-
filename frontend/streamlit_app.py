import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sistema de Triage Hospitalario", page_icon="🏥", layout="wide")

# URL base de la API
API_BASE = "http://127.0.0.1:8000"

# Función para hacer requests
def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE}{endpoint}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE}{endpoint}", json=data)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# Sidebar para navegación
st.sidebar.title("🏥 Triage Hospitalario")
page = st.sidebar.radio("Navegación", ["Inicio", "Admitir Paciente", "Lista de Pacientes", "Siguiente Paciente", "Asignar Cama"])

if page == "Inicio":
    st.title("Bienvenido al Sistema de Triage Hospitalario")
    st.markdown("""
    Este sistema permite gestionar la admisión de pacientes con triage automático basado en síntomas.
    
    **Características:**
    - Triage automático al admitir pacientes
    - Priorización por nivel de urgencia
    - Asignación de camas
    - Historial de reevaluaciones
    """)

elif page == "Admitir Paciente":
    st.title("Admitir Nuevo Paciente")
    with st.form("admit_form"):
        name = st.text_input("Nombre")
        age = st.number_input("Edad", min_value=0, max_value=120)
        symptoms = st.text_area("Síntomas")
        submitted = st.form_submit_button("Admitir")
        if submitted:
            data = {"name": name, "age": age, "symptoms": symptoms}
            result = api_post("/patients/", data)
            if result:
                st.success(f"Paciente {result['name']} admitido con triage {result['triage_level']}")
            else:
                st.error("Error al admitir paciente")

elif page == "Lista de Pacientes":
    st.title("Lista de Pacientes")
    patients = api_get("/patients/")
    if patients:
        df = pd.DataFrame(patients)
        st.dataframe(df)
    else:
        st.warning("No se pudieron cargar los pacientes")

elif page == "Siguiente Paciente":
    st.title("Obtener Siguiente Paciente para Tratamiento")
    if st.button("Obtener Siguiente"):
        patient = api_get("/patients/next")
        if patient:
            st.json(patient)
            st.info(f"Siguiente paciente: {patient['name']} - Nivel: {patient['triage_level']}")
        else:
            st.warning("No hay pacientes esperando")

elif page == "Asignar Cama":
    st.title("Asignar Cama a Paciente")
    patient_id = st.number_input("ID del Paciente", min_value=1)
    if st.button("Asignar Cama"):
        result = api_post(f"/patients/{patient_id}/assign-bed", {})
        if result:
            st.success(f"Cama asignada: {result['name']}")
        else:
            st.error("Error al asignar cama")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Desarrollado con ❤️ para gestión hospitalaria")