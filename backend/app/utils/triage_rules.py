from ..models import TriageLevel

TRIAGE_SYMPTOMS = {
    TriageLevel.RED: {
        "dificultad respiratoria severa",
        "coloracion azul en la piel",
        "frialdad generalizada",
        "traumatismos severos multiples",
        "quemaduras en todo el cuerpo",
        "perdida de miembro u organo",
        "hemorragia masiva", 
    },
    TriageLevel.ORANGE: {
        "alteracion aguda de signos vitales",
        "estado convulsivo",
        "deficiencia respiratoria moderada",
        "crissis hipertensiva",
        "dolor toracico intenso",
        "trauma severo",
        "quemaduras de iii grado"
        "riesgo de perdida de miembro u organo",
        "fracturas",
        "hemorragia moderada",
        "trabajo de parto",
        "ingestion de sustancias toxicas o envenenamiento",
        "dolor agudo",
    },
    TriageLevel.YELLOW: {
        "fiebre mayor a 38.5°c",
        "dificultad respiratoria leve a moderada",
        "fracturas menores",
        "quemaduras de ii grado",
        "trauma moderado",
        "dolor moderado",
        "vomitos o diarrea persistentes",
        "reaccion alergica moderada",
    },
    TriageLevel.GREEN: {
        "dolor leve",
        "tos",
        "resfriado comun",
        "dolor de garganta",
        "cefalea",
        "diarrea leve",
        "vomitos leves",
        "reaccion alergica leve",
    },
    TriageLevel.BLUE: {
        "dolor de cabeza",
        "inapetencia",
        "diarrea cronica",
        "dermatitis",
        "formulacion de medicamentos",
        "lectura de examenes",
        "sintomas agudos sin signos de alarma",
    }
}