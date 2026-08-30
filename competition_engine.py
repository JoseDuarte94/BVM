# ==========================================
# BVM COMPETITION ENGINE
# ==========================================


def calcular_competition_score(datos):

    competencia_directa = datos["competencia_directa"]
    cantidad_competidores = datos["cantidad_competidores"]
    intensidad = datos["intensidad"]
    ventajas_competidores = datos["ventajas_competidores"]
    barreras_entrada = datos["barreras_entrada"]
    diferenciacion = datos["diferenciacion"]

    # ======================================
    # PESOS
    # ======================================

    pesos = {

        "competencia_directa": 0.20,

        "cantidad_competidores": 0.15,

        "intensidad": 0.20,

        "ventajas_competidores": 0.15,

        "barreras_entrada": 0.15,

        "diferenciacion": 0.15
    }

    # ======================================
    # CÁLCULO
    # ======================================

    competition_score = (

        competencia_directa *
        pesos["competencia_directa"]

        +

        cantidad_competidores *
        pesos["cantidad_competidores"]

        +

        intensidad *
        pesos["intensidad"]

        +

        ventajas_competidores *
        pesos["ventajas_competidores"]

        +

        barreras_entrada *
        pesos["barreras_entrada"]

        +

        diferenciacion *
        pesos["diferenciacion"]
    )

    # ======================================
    # INDICADORES
    # ======================================

    indicadores = {

        "Competencia directa":
            competencia_directa,

        "Cantidad de competidores":
            cantidad_competidores,

        "Intensidad competitiva":
            intensidad,

        "Ventajas de competidores":
            ventajas_competidores,

        "Barreras de entrada":
            barreras_entrada,

        "Diferenciación frente a competidores":
            diferenciacion
    }

    # ======================================
    # FORTALEZAS / DEBILIDADES
    # ======================================

    fortalezas = []

    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:

            fortalezas.append(factor)

        elif puntuacion < 60:

            debilidades.append(factor)

    # ======================================
    # ALERTAS
    # ======================================

    alertas = []

    if competencia_directa < 50:

        alertas.append(
            "Existe una presión importante de competidores directos."
        )

    if cantidad_competidores < 50:

        alertas.append(
            "El mercado presenta una cantidad elevada de competidores."
        )

    if intensidad < 50:

        alertas.append(
            "La intensidad competitiva representa una amenaza."
        )

    if ventajas_competidores < 50:

        alertas.append(
            "Los competidores podrían presentar ventajas importantes."
        )

    if barreras_entrada < 50:

        alertas.append(
            "Las barreras de entrada son bajas, facilitando "
            "la aparición de nuevos competidores."
        )

    if diferenciacion < 50:

        alertas.append(
            "La diferenciación frente a los competidores es baja."
        )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if competition_score >= 85:

        diagnostico = (
            "La posición competitiva del proyecto es muy favorable. "
            "El negocio presenta buenas condiciones para competir "
            "dentro de su mercado."
        )

    elif competition_score >= 70:

        diagnostico = (
            "La posición competitiva es favorable, aunque existen "
            "algunos factores que deben fortalecerse para competir "
            "de manera sostenible."
        )

    elif competition_score >= 55:

        diagnostico = (
            "El entorno competitivo presenta riesgos moderados. "
            "Se recomienda fortalecer la diferenciación y analizar "
            "con mayor profundidad a los competidores."
        )

    else:

        diagnostico = (
            "El proyecto enfrenta una presión competitiva importante. "
            "Se recomienda desarrollar una ventaja competitiva clara "
            "antes de realizar una inversión significativa."
        )

    # ======================================
    # RESULTADO
    # ======================================

    return {

        "competition_score": competition_score,

        "indicadores": indicadores,

        "fortalezas": fortalezas,

        "debilidades": debilidades,

        "alertas": alertas,

        "diagnostico": diagnostico
    }