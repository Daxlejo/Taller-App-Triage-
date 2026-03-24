# Sistema de Triage y Flujo de Sala de Urgencias

Este proyecto implementa un sistema de gestión de pacientes en una sala de urgencias hospitalaria, con triage automático y asignación de recursos.

## Estructura del Proyecto

- `backend/`: API REST con FastAPI para la lógica de negocio.
- `frontend/`: Interfaz web con Streamlit.
- `data/`: Base de datos SQLite y migraciones.
- `docs/`: Documentación.

## Instalación

1. Instalar dependencias del backend: `pip install -r backend/requirements.txt`
2. Instalar dependencias del frontend: `pip install -r frontend/requirements.txt`

## Ejecución

- Backend: `uvicorn backend.app.main:app --reload`
- Frontend: `streamlit run frontend/app.py`

## Funcionalidades

- Admisión de pacientes con triage automático.
- Gestión de recursos (camas).
- Dashboard en tiempo real.