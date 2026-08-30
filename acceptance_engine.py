# ==========================================
# BVM ACCEPTANCE ENGINE
# ==========================================


def calcular_acceptance_score(datos):

    intencion = datos["intencion"]
    relevancia = datos["relevancia"]
    disposicion_pago = datos["disposicion_pago"]
    confianza = datos["confianza"]
    facilidad_compra = datos["facilidad_compra"]
    barreras = datos["barreras"]

    # ======================================
    # PESOS
    # ======================================

    pesos = {

        "intencion": 0.25,

        "relevancia": 0.20,

        "disposicion_pago": 0.20,

        "confianza": 0.15,

        "facilidad_compra": 0.10,

        "barreras": 0.10
    }

    # ======================================
    # CÁLCULO
    # ======================================

    acceptance_score = (

        intencion *
        pesos["intencion"]

        +

        relevancia *
        pesos["relevancia"]

        +

        disposicion_pago *
        pesos["disposicion_pago"]

        +

        confianza *
        pesos["confianza"]

        +

        facilidad_compra *
        pesos["facilidad_compra"]

        +

        barreras *
        pesos["barreras"]
    )

    # ======================================
    # INDICADORES
    # ======================================

    indicadores = {

        "Intención de compra":
            intencion,

        "Relevancia":
            relevancia,

        "Disposición a pagar":
            disposicion_pago,

        "Confianza":
            confianza,

        "Facilidad de compra":
            facilidad_compra,

        "Bajas barreras de compra":
            barreras
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

    if intencion < 50:

        alertas.append(
            "La intención de compra es baja."
        )

    if disposicion_pago < 50:

        alertas.append(
            "Existe una posible resistencia al precio."
        )

    if confianza < 50:

        alertas.append(
            "La confianza en el producto o marca es baja."
        )

    if barreras < 50:

        alertas.append(
            "Existen barreras importantes para realizar la compra."
        )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if acceptance_score >= 85:

        diagnostico = (
            "Existe una aceptación potencial muy alta. "
            "Los consumidores muestran una combinación "
            "favorable de intención de compra, relevancia "
            "y disposición a pagar."
        )

    elif acceptance_score >= 70:

        diagnostico = (
            "El producto presenta una aceptación potencial "
            "favorable, aunque existen factores que deben "
            "fortalecerse."
        )

    elif acceptance_score >= 55:

        diagnostico = (
            "La aceptación potencial es moderada. "
            "Se recomienda realizar pruebas de mercado."
        )

    else:

        diagnostico = (
            "La aceptación potencial es baja. "
            "La propuesta necesita modificaciones."
        )

    # ======================================
    # RESULTADO
    # ======================================

    return {

        "acceptance_score": acceptance_score,

        "indicadores": indicadores,

        "fortalezas": fortalezas,

        "debilidades": debilidades,

        "alertas": alertas,

        "diagnostico": diagnostico
    }