# ==========================================
# BVM CUSTOMER ENGINE
# ==========================================


def calcular_customer_score(datos):

    definicion_cliente = datos["definicion_cliente"]
    necesidad = datos["necesidad"]
    capacidad_pago = datos["capacidad_pago"]
    accesibilidad = datos["accesibilidad"]
    frecuencia = datos["frecuencia"]
    tamano_segmento = datos["tamano_segmento"]

    # ======================================
    # PESOS
    # ======================================

    pesos = {

        "definicion_cliente": 0.15,

        "necesidad": 0.25,

        "capacidad_pago": 0.20,

        "accesibilidad": 0.15,

        "frecuencia": 0.15,

        "tamano_segmento": 0.10
    }

    # ======================================
    # CÁLCULO
    # ======================================

    customer_score = (

        definicion_cliente *
        pesos["definicion_cliente"]

        +

        necesidad *
        pesos["necesidad"]

        +

        capacidad_pago *
        pesos["capacidad_pago"]

        +

        accesibilidad *
        pesos["accesibilidad"]

        +

        frecuencia *
        pesos["frecuencia"]

        +

        tamano_segmento *
        pesos["tamano_segmento"]
    )

    # ======================================
    # INDICADORES
    # ======================================

    indicadores = {

        "Definición del cliente":
            definicion_cliente,

        "Necesidad":
            necesidad,

        "Capacidad de pago":
            capacidad_pago,

        "Accesibilidad":
            accesibilidad,

        "Frecuencia de compra":
            frecuencia,

        "Tamaño del segmento":
            tamano_segmento
    }

    # ======================================
    # FORTALEZAS
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

    if definicion_cliente < 50:

        alertas.append(
            "El segmento de clientes no está claramente definido."
        )

    if capacidad_pago < 50:

        alertas.append(
            "La capacidad de pago del cliente objetivo podría ser limitada."
        )

    if accesibilidad < 50:

        alertas.append(
            "El cliente objetivo puede ser difícil de alcanzar."
        )

    if frecuencia < 50:

        alertas.append(
            "La frecuencia potencial de compra es baja."
        )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if customer_score >= 85:

        diagnostico = (
            "El cliente objetivo presenta características "
            "muy favorables para el negocio."
        )

    elif customer_score >= 70:

        diagnostico = (
            "El segmento objetivo es atractivo, aunque "
            "algunos factores deben ser fortalecidos."
        )

    elif customer_score >= 55:

        diagnostico = (
            "El segmento presenta potencial moderado y "
            "requiere mayor validación."
        )

    else:

        diagnostico = (
            "El segmento presenta características poco "
            "favorables para el proyecto."
        )

    # ======================================
    # RESULTADO
    # ======================================

    return {

        "customer_score": customer_score,

        "indicadores": indicadores,

        "fortalezas": fortalezas,

        "debilidades": debilidades,

        "alertas": alertas,

        "diagnostico": diagnostico
    }