# ==========================================
# BVM POSITIONING ENGINE
# ==========================================


def calcular_positioning_score(datos):

    claridad_marca = datos["claridad_marca"]
    propuesta_valor = datos["propuesta_valor"]
    diferenciacion = datos["diferenciacion"]
    posicionamiento_precio = datos["posicionamiento_precio"]
    reconocimiento = datos["reconocimiento"]
    coherencia = datos["coherencia"]

    # ======================================
    # PESOS
    # ======================================

    pesos = {

        "claridad_marca": 0.20,
        "propuesta_valor": 0.25,
        "diferenciacion": 0.20,
        "posicionamiento_precio": 0.10,
        "reconocimiento": 0.10,
        "coherencia": 0.15
    }

    # ======================================
    # CÁLCULO
    # ======================================

    positioning_score = (

        claridad_marca *
        pesos["claridad_marca"]

        +

        propuesta_valor *
        pesos["propuesta_valor"]

        +

        diferenciacion *
        pesos["diferenciacion"]

        +

        posicionamiento_precio *
        pesos["posicionamiento_precio"]

        +

        reconocimiento *
        pesos["reconocimiento"]

        +

        coherencia *
        pesos["coherencia"]
    )

    # ======================================
    # INDICADORES
    # ======================================

    indicadores = {

        "Claridad de marca":
            claridad_marca,

        "Propuesta de valor":
            propuesta_valor,

        "Diferenciación":
            diferenciacion,

        "Posicionamiento de precio":
            posicionamiento_precio,

        "Reconocimiento de marca":
            reconocimiento,

        "Coherencia del posicionamiento":
            coherencia
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

    if claridad_marca < 50:

        alertas.append(
            "La identidad de marca no está claramente definida."
        )

    if propuesta_valor < 50:

        alertas.append(
            "La propuesta de valor presenta poca claridad."
        )

    if diferenciacion < 50:

        alertas.append(
            "El negocio presenta una diferenciación limitada."
        )

    if posicionamiento_precio < 50:

        alertas.append(
            "El posicionamiento de precio podría no ser adecuado "
            "para el mercado objetivo."
        )

    if reconocimiento < 50:

        alertas.append(
            "El reconocimiento de marca es bajo."
        )

    if coherencia < 50:

        alertas.append(
            "Existe poca coherencia entre la marca, producto "
            "y mercado objetivo."
        )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if positioning_score >= 85:

        diagnostico = (
            "El negocio presenta un posicionamiento muy sólido. "
            "La propuesta de valor, diferenciación y marca "
            "permiten construir una posición competitiva clara."
        )

    elif positioning_score >= 70:

        diagnostico = (
            "El negocio presenta un posicionamiento favorable, "
            "aunque algunos elementos pueden fortalecerse para "
            "construir una ventaja competitiva más sostenible."
        )

    elif positioning_score >= 55:

        diagnostico = (
            "El posicionamiento presenta potencial, pero requiere "
            "mayor claridad en la propuesta de valor y diferenciación."
        )

    else:

        diagnostico = (
            "El posicionamiento presenta debilidades importantes. "
            "Se recomienda redefinir la propuesta de valor, marca "
            "y diferenciación antes de continuar."
        )

    # ======================================
    # RESULTADO
    # ======================================

    return {

        "positioning_score": positioning_score,

        "indicadores": indicadores,

        "fortalezas": fortalezas,

        "debilidades": debilidades,

        "alertas": alertas,

        "diagnostico": diagnostico
    }