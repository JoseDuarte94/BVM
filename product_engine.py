# ==========================================
# BVM PRODUCT ENGINE
# ==========================================


def calcular_product_score(datos):

    necesidad = datos["necesidad"]
    valor_percibido = datos["valor_percibido"]
    diferenciacion = datos["diferenciacion"]
    calidad = datos["calidad"]
    innovacion = datos["innovacion"]
    sustitucion = datos["sustitucion"]

    # ======================================
    # PESOS
    # ======================================

    pesos = {
        "necesidad": 0.25,
        "valor_percibido": 0.25,
        "diferenciacion": 0.20,
        "calidad": 0.15,
        "innovacion": 0.05,
        "sustitucion": 0.10
    }

    # ======================================
    # CÁLCULO
    # ======================================

    product_score = (
        necesidad * pesos["necesidad"] +
        valor_percibido * pesos["valor_percibido"] +
        diferenciacion * pesos["diferenciacion"] +
        calidad * pesos["calidad"] +
        innovacion * pesos["innovacion"] +
        sustitucion * pesos["sustitucion"]
    )

    # ======================================
    # INDICADORES
    # ======================================

    indicadores = {

        "Necesidad": necesidad,

        "Valor percibido": valor_percibido,

        "Diferenciación": diferenciacion,

        "Calidad": calidad,

        "Innovación": innovacion,

        "Dificultad de sustitución": sustitucion
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

    if necesidad < 50:

        alertas.append(
            "El producto resuelve una necesidad relativamente débil."
        )

    if diferenciacion < 50:

        alertas.append(
            "La diferenciación frente a alternativas existentes es baja."
        )

    if calidad < 50:

        alertas.append(
            "La calidad percibida podría representar una barrera."
        )

    if sustitucion < 50:

        alertas.append(
            "El producto puede ser fácilmente sustituido."
        )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if product_score >= 85:

        diagnostico = (
            "El producto presenta una propuesta muy fuerte. "
            "Existe una combinación favorable de necesidad, "
            "valor y diferenciación."
        )

    elif product_score >= 70:

        diagnostico = (
            "El producto presenta una propuesta atractiva, "
            "aunque existen factores que podrían fortalecerse."
        )

    elif product_score >= 55:

        diagnostico = (
            "El producto presenta potencial, pero requiere "
            "mayor validación antes de una inversión importante."
        )

    else:

        diagnostico = (
            "El producto presenta debilidades importantes. "
            "Se recomienda modificar la propuesta."
        )

    # ======================================
    # RESULTADO
    # ======================================

    return {

        "product_score": product_score,

        "indicadores": indicadores,

        "fortalezas": fortalezas,

        "debilidades": debilidades,

        "alertas": alertas,

        "diagnostico": diagnostico
    }