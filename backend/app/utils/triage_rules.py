from ..models.triage import TriageStatus

TRIAGE_SYMPTOMS = {
    TriageStatus.RED: {
        "Dificultad respiratoria severa",
        "Coloracion azul en la piel",
        "Frialdad generalizada",
        "Traumatismos severos multiples",
        "Quemaduras en todo el cuerpo",
        "Perdida de miembro u organo",
        "Hemorragia masiva", 
    },
    TriageStatus.ORANGE: {
        "Alteracion aguda de signos vitales",
        "Estado convulsivo",
        "Deficiencia respiratoria moderada",
        "Crissis hipertensiva",
        "Dolor toracico intenso",
        "Trauma severo",
        "Quemaduras de III grado"
        "Riesgo de perdida de miembro u organo",
        "Fracturas",
        "Hemorragia moderada",
        "Trabajo de parto",
        "Ingestión de sustancias toxicas o envenenamiento",
        "Dolor agudo",
    },
    TriageStatus.YELLOW: {
        "Fiebre mayor a 38.5°C",
        "Dificultad respiratoria leve a moderada",
        "Fracturas menores",
        "Quemaduras de II grado",
        "Trauma moderado",
        "Dolor moderado",
        "Vomitos o diarrea persistentes",
        "Reaccion alergica moderada",
    },
    TriageStatus.GREEN: {
        "Dolor leve",
        "Tos",
        "Resfriado comun",
        "Dolor de garganta",
        "Cefalea leve",
        "Diarrea leve",
        "Vomitos leves",
        "Reaccion alergica leve",
    },
    TriageStatus.BLUE: {
        "Dolor de cabeza",
        "Inapetencia",
        "Diarrea cronica",
        "Dermatitis",
        "Formulacion de medicamentos",
        "Lectura de examenes",
        "Sintomas agudos sin signos de alarma",
    }
}