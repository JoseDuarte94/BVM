# ==========================================
# BVM MARKET ENGINE
# Version 3.0
# ==========================================


def calcular_market_score(datos):
    """
    Calcula el Market Score a partir de
    datos cuantitativos del mercado.
    """

    poblacion = datos["poblacion"]
    porcentaje_objetivo = datos["porcentaje_objetivo"]
    frecuencia_compra = datos["frecuencia_compra"]
    ventas_estimadas = datos["ventas_estimadas"]
    crecimiento = datos["crecimiento"]
    accesibilidad = datos["accesibilidad"]


    # --------------------------------------
    # MERCADO OBJETIVO
    # --------------------------------------

    mercado_objetivo = (
        poblacion *
        (porcentaje_objetivo / 100)
    )


    # --------------------------------------
    # DEMANDA POTENCIAL
    # --------------------------------------

    demanda_potencial = (
        mercado_objetivo *
        frecuencia_compra
    )


    # --------------------------------------
    # COBERTURA DEL MERCADO
    # --------------------------------------

    if demanda_potencial > 0:

        cobertura = (
            ventas_estimadas /
            demanda_potencial
        ) * 100

    else:

        cobertura = 0


    # --------------------------------------
    # SCORE DE COBERTURA
    # --------------------------------------

    if cobertura >= 50:

        score_cobertura = 100

    elif cobertura >= 35:

        score_cobertura = 90

    elif cobertura >= 25:

        score_cobertura = 80

    elif cobertura >= 15:

        score_cobertura = 70

    elif cobertura >= 10:

        score_cobertura = 60

    elif cobertura >= 5:

        score_cobertura = 45

    else:

        score_cobertura = 25


    # --------------------------------------
    # SCORE DE CRECIMIENTO
    # --------------------------------------

    if crecimiento >= 10:

        score_crecimiento = 100

    elif crecimiento >= 7:

        score_crecimiento = 90

    elif crecimiento >= 5:

        score_crecimiento = 80

    elif crecimiento >= 3:

        score_crecimiento = 70

    elif crecimiento >= 1:

        score_crecimiento = 60

    else:

        score_crecimiento = 40


    # --------------------------------------
    # SCORE DE ACCESIBILIDAD
    # --------------------------------------

    if accesibilidad >= 80:

        score_accesibilidad = 100

    elif accesibilidad >= 60:

        score_accesibilidad = 85

    elif accesibilidad >= 40:

        score_accesibilidad = 70

    elif accesibilidad >= 20:

        score_accesibilidad = 55

    else:

        score_accesibilidad = 35


    # --------------------------------------
    # SCORE FINAL
    # --------------------------------------

    market_score = (

        score_cobertura * 0.50 +

        score_crecimiento * 0.30 +

        score_accesibilidad * 0.20

    )


    # --------------------------------------
    # ALERTAS
    # --------------------------------------

    alertas = []


    if ventas_estimadas > demanda_potencial:

        alertas.append(
            "Las ventas proyectadas superan "
            "la demanda potencial estimada."
        )


    if cobertura < 5:

        alertas.append(
            "La cobertura estimada del mercado "
            "es muy baja."
        )


    if crecimiento < 2:

        alertas.append(
            "El crecimiento estimado del mercado "
            "es bajo."
        )


    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    return {

        "mercado_objetivo": mercado_objetivo,

        "demanda_potencial": demanda_potencial,

        "cobertura": cobertura,

        "score_cobertura": score_cobertura,

        "score_crecimiento": score_crecimiento,

        "score_accesibilidad": score_accesibilidad,

        "market_score": market_score,

        "alertas": alertas
    }