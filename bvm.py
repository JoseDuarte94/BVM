# ==========================================
# BUSINESS VALIDATION MODEL
# Version 0.4
# BVM ENGINE
# ==========================================

from bvm_engine import analizar_negocio
from database import (
    inicializar_base_datos,
    guardar_negocio,
    mostrar_negocios
)

inicializar_base_datos()

print()
print("==========================================")
print("       BUSINESS VALIDATION MODEL")
print("==========================================")
print()

print("1. Analizar nuevo negocio")
print("2. Ver proyectos guardados")
print()

opcion = input("Seleccione una opción: ")

if opcion == "2":

    mostrar_negocios()

    exit()


# ------------------------------------------
# FUNCIÓN PARA CALCULAR UNA PUNTUACIÓN
# ------------------------------------------

def calcular_score(indicadores, pesos):

    resultado = 0

    for indicador, peso in zip(indicadores, pesos):
        resultado += indicador * peso

    return resultado


def calcular_product_score():

    print()
    print("==========================================")
    print("          EVALUACIÓN DEL PRODUCTO")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Muy bajo")
    print("1 = Bajo")
    print("2 = Regular")
    print("3 = Medio")
    print("4 = Alto")
    print("5 = Muy alto")
    print()

    # --------------------------------------
    # PREGUNTAS
    # --------------------------------------

    necesidad = float(input(
        "¿Qué tan fuerte es la necesidad que resuelve?: "
    ))

    valor = float(input(
        "¿Qué tan alto es el valor percibido?: "
    ))

    diferenciacion = float(input(
        "¿Qué tan diferenciado es el producto?: "
    ))

    calidad = float(input(
        "¿Qué tan alta es la calidad esperada?: "
    ))

    innovacion = float(input(
        "¿Qué tan innovador es el producto?: "
    ))

    sustitucion = float(input(
        "¿Qué tan difícil es sustituirlo?: "
    ))

    # --------------------------------------
    # CONVERTIR 0-5 A 0-100
    # --------------------------------------

    indicadores = {
        "Necesidad": necesidad * 20,
        "Valor percibido": valor * 20,
        "Diferenciación": diferenciacion * 20,
        "Calidad": calidad * 20,
        "Innovación": innovacion * 20,
        "Dificultad de sustitución": sustitucion * 20
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Necesidad": 0.25,
        "Valor percibido": 0.25,
        "Diferenciación": 0.20,
        "Calidad": 0.15,
        "Innovación": 0.05,
        "Dificultad de sustitución": 0.10
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    product_score = 0

    for factor in indicadores:
        product_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # IDENTIFICAR FORTALEZAS Y DEBILIDADES
    # --------------------------------------

    fortalezas = []
    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            debilidades.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("          ANÁLISIS DEL PRODUCTO")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"PRODUCT SCORE: {product_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("FORTALEZAS")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron fortalezas sobresalientes.")

    print()
    print("DEBILIDADES")
    print("------------------------------------------")

    if debilidades:
        for debilidad in debilidades:
            print(f"[-] {debilidad}")
    else:
        print("No se identificaron debilidades importantes.")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO")
    print("------------------------------------------")

    if product_score >= 85:

        print(
            "El producto presenta una propuesta muy fuerte. "
            "Existe una combinación favorable de necesidad, "
            "valor y diferenciación."
        )

    elif product_score >= 70:

        print(
            "El producto presenta una propuesta atractiva, "
            "aunque existen elementos que podrían fortalecerse "
            "antes de realizar una inversión importante."
        )

    elif product_score >= 55:

        print(
            "El producto presenta potencial, pero necesita "
            "mayor validación antes de ser considerado "
            "comercialmente sólido."
        )

    else:

        print(
            "El producto presenta debilidades importantes. "
            "Se recomienda modificar la propuesta antes "
            "de continuar con el proyecto."
        )

    return product_score


def calcular_market_score():

    print()
    print("==========================================")
    print("            EVALUACIÓN DEL MERCADO")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Muy bajo")
    print("1 = Bajo")
    print("2 = Regular")
    print("3 = Medio")
    print("4 = Alto")
    print("5 = Muy alto")
    print()

    tamano = float(input(
        "¿Qué tan grande es el mercado potencial?: "
    ))

    demanda = float(input(
        "¿Qué tan fuerte es la demanda?: "
    ))

    crecimiento = float(input(
        "¿Qué tan rápido está creciendo el mercado?: "
    ))

    tendencia = float(input(
        "¿Qué tan favorable es la tendencia del mercado?: "
    ))

    accesibilidad = float(input(
        "¿Qué tan fácil es acceder al mercado?: "
    ))

    estabilidad = float(input(
        "¿Qué tan estable es el mercado?: "
    ))

    # --------------------------------------
    # CONVERTIR 0-5 A 0-100
    # --------------------------------------

    indicadores = {
        "Tamaño del mercado": tamano * 20,
        "Demanda": demanda * 20,
        "Crecimiento": crecimiento * 20,
        "Tendencia": tendencia * 20,
        "Accesibilidad": accesibilidad * 20,
        "Estabilidad": estabilidad * 20
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Tamaño del mercado": 0.25,
        "Demanda": 0.25,
        "Crecimiento": 0.15,
        "Tendencia": 0.15,
        "Accesibilidad": 0.10,
        "Estabilidad": 0.10
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    market_score = 0

    for factor in indicadores:
        market_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # FORTALEZAS Y DEBILIDADES
    # --------------------------------------

    fortalezas = []
    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            debilidades.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("            ANÁLISIS DEL MERCADO")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"MARKET SCORE: {market_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("FORTALEZAS DEL MERCADO")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron fortalezas sobresalientes.")

    print()
    print("DEBILIDADES DEL MERCADO")
    print("------------------------------------------")

    if debilidades:
        for debilidad in debilidades:
            print(f"[-] {debilidad}")
    else:
        print("No se identificaron debilidades importantes.")

    print()
    print("DIAGNÓSTICO DEL MERCADO")
    print("------------------------------------------")
    print()

    if market_score >= 85:

        print(
            "El mercado presenta condiciones muy favorables. "
            "Existe una combinación fuerte de demanda, tamaño "
            "y perspectivas de crecimiento."
        )

    elif market_score >= 70:

        print(
            "El mercado presenta condiciones favorables, "
            "aunque existen algunos factores que deben "
            "analizarse antes de realizar una inversión importante."
        )

    elif market_score >= 55:

        print(
            "El mercado presenta potencial moderado. "
            "Se requiere investigación adicional para "
            "determinar si existe suficiente oportunidad."
        )

    else:

        print(
            "El mercado presenta condiciones poco favorables. "
            "Se recomienda analizar otros segmentos o modificar "
            "la propuesta de negocio."
        )

    return market_score


def calcular_customer_score():

    print()
    print("==========================================")
    print("          EVALUACIÓN DEL CLIENTE")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Muy bajo")
    print("1 = Bajo")
    print("2 = Regular")
    print("3 = Medio")
    print("4 = Alto")
    print("5 = Muy alto")
    print()

    publico = float(input(
        "¿Qué tan grande es el público objetivo?: "
    ))

    capacidad_pago = float(input(
        "¿Qué tan alta es la capacidad de pago del cliente?: "
    ))

    frecuencia = float(input(
        "¿Qué tan frecuente podría consumir el producto?: "
    ))

    necesidad = float(input(
        "¿Qué tan fuerte es la necesidad del cliente?: "
    ))

    acceso = float(input(
        "¿Qué tan fácil es llegar al cliente?: "
    ))

    fidelizacion = float(input(
        "¿Qué tan probable es que el cliente vuelva a comprar?: "
    ))

    # --------------------------------------
    # CONVERTIR 0-5 A 0-100
    # --------------------------------------

    indicadores = {
        "Público objetivo": publico * 20,
        "Capacidad de pago": capacidad_pago * 20,
        "Frecuencia de consumo": frecuencia * 20,
        "Necesidad": necesidad * 20,
        "Acceso al cliente": acceso * 20,
        "Fidelización": fidelizacion * 20
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Público objetivo": 0.20,
        "Capacidad de pago": 0.20,
        "Frecuencia de consumo": 0.20,
        "Necesidad": 0.20,
        "Acceso al cliente": 0.10,
        "Fidelización": 0.10
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    customer_score = 0

    for factor in indicadores:
        customer_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # FORTALEZAS Y DEBILIDADES
    # --------------------------------------

    fortalezas = []
    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            debilidades.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("           ANÁLISIS DEL CLIENTE")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"CUSTOMER SCORE: {customer_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("FORTALEZAS DEL CLIENTE")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron fortalezas sobresalientes.")

    print()
    print("DEBILIDADES DEL CLIENTE")
    print("------------------------------------------")

    if debilidades:
        for debilidad in debilidades:
            print(f"[-] {debilidad}")
    else:
        print("No se identificaron debilidades importantes.")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO DEL CLIENTE")
    print("------------------------------------------")

    if customer_score >= 85:

        print(
            "El perfil del cliente es muy favorable. "
            "Existe un público atractivo con buena capacidad "
            "de compra y potencial de consumo recurrente."
        )

    elif customer_score >= 70:

        print(
            "Existe un perfil de cliente favorable, aunque "
            "algunos factores deben fortalecerse para aumentar "
            "el potencial comercial."
        )

    elif customer_score >= 55:

        print(
            "El perfil del cliente presenta potencial moderado. "
            "Se necesita mayor investigación sobre hábitos, "
            "capacidad de pago y frecuencia de compra."
        )

    else:

        print(
            "El perfil del cliente presenta debilidades importantes. "
            "Se recomienda revisar el público objetivo y la "
            "propuesta de valor."
        )

    return customer_score

def calcular_acceptance_score():

    print()
    print("==========================================")
    print("         EVALUACIÓN DE ACEPTACIÓN")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Muy bajo")
    print("1 = Bajo")
    print("2 = Regular")
    print("3 = Medio")
    print("4 = Alto")
    print("5 = Muy alto")
    print()

    interes = float(input(
        "¿Qué tan alto es el interés del consumidor?: "
    ))

    intencion = float(input(
        "¿Qué tan alta es la intención de compra?: "
    ))

    precio = float(input(
        "¿Qué tan aceptado es el precio propuesto?: "
    ))

    preferencia = float(input(
        "¿Qué tan preferido es el producto frente a alternativas?: "
    ))

    prueba = float(input(
        "¿Qué tan alta es la disposición a probarlo?: "
    ))

    compra = float(input(
        "¿Qué tan alta es la evidencia de compra real?: "
    ))

    recompra = float(input(
        "¿Qué tan probable es la recompra?: "
    ))

    # --------------------------------------
    # CONVERTIR 0-5 A 0-100
    # --------------------------------------

    indicadores = {
        "Interés": interes * 20,
        "Intención de compra": intencion * 20,
        "Aceptación del precio": precio * 20,
        "Preferencia": preferencia * 20,
        "Disposición a probar": prueba * 20,
        "Compra real": compra * 20,
        "Recompra": recompra * 20
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Interés": 0.15,
        "Intención de compra": 0.25,
        "Aceptación del precio": 0.15,
        "Preferencia": 0.15,
        "Disposición a probar": 0.10,
        "Compra real": 0.15,
        "Recompra": 0.05
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    acceptance_score = 0

    for factor in indicadores:
        acceptance_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # FORTALEZAS Y DEBILIDADES
    # --------------------------------------

    fortalezas = []
    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            debilidades.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("        ANÁLISIS DE ACEPTACIÓN")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"ACCEPTANCE SCORE: {acceptance_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("FORTALEZAS")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron fortalezas sobresalientes.")

    print()
    print("DEBILIDADES")
    print("------------------------------------------")

    if debilidades:
        for debilidad in debilidades:
            print(f"[-] {debilidad}")
    else:
        print("No se identificaron debilidades importantes.")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO DE ACEPTACIÓN")
    print("------------------------------------------")

    if acceptance_score >= 85:

        print(
            "Existe evidencia muy favorable de aceptación. "
            "Los consumidores muestran interés, intención de compra "
            "y señales de comportamiento comercial."
        )

    elif acceptance_score >= 70:

        print(
            "La aceptación es favorable, aunque todavía existen "
            "elementos que deberían validarse mediante pruebas "
            "con consumidores reales."
        )

    elif acceptance_score >= 55:

        print(
            "La aceptación presenta señales moderadas. "
            "Se recomienda realizar encuestas, pruebas piloto "
            "o ventas experimentales."
        )

    else:

        print(
            "La evidencia de aceptación es débil. "
            "Se recomienda validar nuevamente la propuesta "
            "antes de realizar una inversión significativa."
        )

    return acceptance_score

def calcular_competition_score():

    print()
    print("==========================================")
    print("        EVALUACIÓN DE LA COMPETENCIA")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Muy bajo")
    print("1 = Bajo")
    print("2 = Regular")
    print("3 = Medio")
    print("4 = Alto")
    print("5 = Muy alto")
    print()

    intensidad = float(input(
        "¿Qué tan intensa es la competencia?: "
    ))

    saturacion = float(input(
        "¿Qué tan saturado está el mercado?: "
    ))

    diferenciacion = float(input(
        "¿Qué tan diferenciado está nuestro negocio?: "
    ))

    barreras = float(input(
        "¿Qué tan altas son las barreras de entrada?: "
    ))

    poder = float(input(
        "¿Qué tan fuerte es el poder de los competidores?: "
    ))

    capacidad = float(input(
        "¿Qué tan capaz es nuestro negocio de competir?: "
    ))

    # --------------------------------------
    # CONVERTIR 0-5 A 0-100
    # --------------------------------------

    # En estos factores:
    # MAYOR = MEJOR
    diferenciacion_score = diferenciacion * 20
    barreras_score = barreras * 20
    capacidad_score = capacidad * 20

    # En estos factores:
    # MENOR = MEJOR
    intensidad_score = (5 - intensidad) * 20
    saturacion_score = (5 - saturacion) * 20
    poder_score = (5 - poder) * 20

    indicadores = {
        "Intensidad competitiva": intensidad_score,
        "Saturación del mercado": saturacion_score,
        "Diferenciación": diferenciacion_score,
        "Barreras de entrada": barreras_score,
        "Poder de los competidores": poder_score,
        "Capacidad de competir": capacidad_score
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Intensidad competitiva": 0.20,
        "Saturación del mercado": 0.15,
        "Diferenciación": 0.25,
        "Barreras de entrada": 0.15,
        "Poder de los competidores": 0.15,
        "Capacidad de competir": 0.10
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    competition_score = 0

    for factor in indicadores:
        competition_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # FORTALEZAS Y DEBILIDADES
    # --------------------------------------

    fortalezas = []
    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            debilidades.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("       ANÁLISIS DE LA COMPETENCIA")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"COMPETITION SCORE: {competition_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("FORTALEZAS COMPETITIVAS")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron fortalezas sobresalientes.")

    print()
    print("DEBILIDADES COMPETITIVAS")
    print("------------------------------------------")

    if debilidades:
        for debilidad in debilidades:
            print(f"[-] {debilidad}")
    else:
        print("No se identificaron debilidades importantes.")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO COMPETITIVO")
    print("------------------------------------------")

    if competition_score >= 85:

        print(
            "El entorno competitivo es muy favorable. "
            "El negocio presenta una posición diferenciada "
            "y buenas condiciones para competir."
        )

    elif competition_score >= 70:

        print(
            "El negocio presenta una posición competitiva favorable, "
            "aunque deberá desarrollar ventajas claras frente "
            "a los competidores existentes."
        )

    elif competition_score >= 55:

        print(
            "La posición competitiva presenta dificultades moderadas. "
            "Se requiere estudiar cuidadosamente a los competidores "
            "y fortalecer la propuesta de valor."
        )

    else:

        print(
            "El entorno competitivo presenta riesgos importantes. "
            "Se recomienda revisar la diferenciación y las barreras "
            "antes de realizar una inversión significativa."
        )

    return competition_score

def calcular_positioning_score():

    print()
    print("==========================================")
    print("        EVALUACIÓN DEL POSICIONAMIENTO")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Muy bajo")
    print("1 = Bajo")
    print("2 = Regular")
    print("3 = Medio")
    print("4 = Alto")
    print("5 = Muy alto")
    print()

    claridad = float(input(
        "¿Qué tan clara es la propuesta de valor?: "
    ))

    diferenciacion = float(input(
        "¿Qué tan diferenciado está el negocio?: "
    ))

    valor_precio = float(input(
        "¿Qué tan buena es la relación valor/precio?: "
    ))

    identidad = float(input(
        "¿Qué tan fuerte es la identidad de marca?: "
    ))

    segmentacion = float(input(
        "¿Qué tan bien definido está el público objetivo?: "
    ))

    comunicacion = float(input(
        "¿Qué tan efectiva es la comunicación de la propuesta?: "
    ))

    # --------------------------------------
    # CONVERTIR 0-5 A 0-100
    # --------------------------------------

    indicadores = {
        "Claridad de propuesta": claridad * 20,
        "Diferenciación": diferenciacion * 20,
        "Relación valor/precio": valor_precio * 20,
        "Identidad de marca": identidad * 20,
        "Segmentación": segmentacion * 20,
        "Comunicación": comunicacion * 20
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Claridad de propuesta": 0.20,
        "Diferenciación": 0.25,
        "Relación valor/precio": 0.20,
        "Identidad de marca": 0.15,
        "Segmentación": 0.10,
        "Comunicación": 0.10
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    positioning_score = 0

    for factor in indicadores:
        positioning_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # FORTALEZAS Y DEBILIDADES
    # --------------------------------------

    fortalezas = []
    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            debilidades.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("       ANÁLISIS DEL POSICIONAMIENTO")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"POSITIONING SCORE: {positioning_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("FORTALEZAS DE POSICIONAMIENTO")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron fortalezas sobresalientes.")

    print()
    print("DEBILIDADES DE POSICIONAMIENTO")
    print("------------------------------------------")

    if debilidades:
        for debilidad in debilidades:
            print(f"[-] {debilidad}")
    else:
        print("No se identificaron debilidades importantes.")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO DEL POSICIONAMIENTO")
    print("------------------------------------------")

    if positioning_score >= 85:

        print(
            "El negocio presenta un posicionamiento muy fuerte. "
            "La propuesta de valor es clara, diferenciada y "
            "bien dirigida hacia su público objetivo."
        )

    elif positioning_score >= 70:

        print(
            "El posicionamiento es favorable, aunque existen "
            "elementos que pueden fortalecerse para lograr "
            "una ventaja más clara frente a los competidores."
        )

    elif positioning_score >= 55:

        print(
            "El posicionamiento presenta potencial moderado. "
            "Se recomienda mejorar la propuesta de valor, "
            "segmentación y diferenciación."
        )

    else:

        print(
            "El posicionamiento presenta debilidades importantes. "
            "El negocio necesita definir con mayor claridad "
            "a quién sirve y por qué debería ser elegido."
        )

    return positioning_score

def calcular_financial_score():

    print()
    print("==========================================")
    print("          ANÁLISIS FINANCIERO")
    print("==========================================")
    print()

    print("Introduzca los datos estimados del negocio.")
    print("Utilice valores mensuales cuando se indique.")
    print()

    # --------------------------------------
    # DATOS DEL NEGOCIO
    # --------------------------------------

    inversion = float(input(
        "Inversión inicial (L): "
    ))

    precio = float(input(
        "Precio promedio de venta por unidad (L): "
    ))

    ventas_mensuales = float(input(
        "Unidades vendidas mensualmente: "
    ))

    costo_variable = float(input(
        "Costo variable por unidad (L): "
    ))

    costos_fijos = float(input(
        "Costos fijos mensuales (L): "
    ))

    # --------------------------------------
    # VALIDACIONES
    # --------------------------------------

    if inversion <= 0:
        print("La inversión inicial debe ser mayor que 0.")
        return 0

    if precio <= 0:
        print("El precio debe ser mayor que 0.")
        return 0

    if ventas_mensuales < 0:
        print("Las ventas no pueden ser negativas.")
        return 0

    if costo_variable < 0:
        print("El costo variable no puede ser negativo.")
        return 0

    if costos_fijos < 0:
        print("Los costos fijos no pueden ser negativos.")
        return 0

    if costo_variable >= precio:

        print()
        print("ADVERTENCIA")
        print("------------------------------------------")
        print(
            "El costo variable es igual o superior al precio "
            "de venta. No existe margen de contribución positivo."
        )

        return 0

    # --------------------------------------
    # CÁLCULOS
    # --------------------------------------

    ingresos_mensuales = precio * ventas_mensuales

    costos_variables_totales = (
        costo_variable * ventas_mensuales
    )

    margen_contribucion_unitario = (
        precio - costo_variable
    )

    margen_contribucion_total = (
        margen_contribucion_unitario *
        ventas_mensuales
    )

    utilidad_operativa = (
        ingresos_mensuales
        - costos_variables_totales
        - costos_fijos
    )

    margen_operativo = (
        utilidad_operativa / ingresos_mensuales
        if ingresos_mensuales > 0
        else 0
    )

    # --------------------------------------
    # PUNTO DE EQUILIBRIO
    # --------------------------------------

    punto_equilibrio_unidades = (
        costos_fijos /
        margen_contribucion_unitario
    )

    punto_equilibrio_ventas = (
        punto_equilibrio_unidades * precio
    )

    # --------------------------------------
    # PROYECCIÓN ANUAL
    # --------------------------------------

    utilidad_anual = utilidad_operativa * 12

    roi_anual = (
        utilidad_anual / inversion
        if inversion > 0
        else 0
    )

    # --------------------------------------
    # PAYBACK
    # --------------------------------------

    if utilidad_operativa > 0:

        payback_meses = (
            inversion / utilidad_operativa
        )

    else:

        payback_meses = None

    # --------------------------------------
    # FINANCIAL SCORE
    # --------------------------------------

    # Margen operativo
    if margen_operativo >= 0.30:
        margen_score = 100

    elif margen_operativo >= 0.20:
        margen_score = 85

    elif margen_operativo >= 0.10:
        margen_score = 70

    elif margen_operativo > 0:
        margen_score = 55

    else:
        margen_score = 20

    # ROI
    if roi_anual >= 0.40:
        roi_score = 100

    elif roi_anual >= 0.25:
        roi_score = 85

    elif roi_anual >= 0.15:
        roi_score = 70

    elif roi_anual > 0:
        roi_score = 55

    else:
        roi_score = 20

    # Cobertura del punto de equilibrio
    if ventas_mensuales >= punto_equilibrio_unidades * 2:
        equilibrio_score = 100

    elif ventas_mensuales >= punto_equilibrio_unidades * 1.5:
        equilibrio_score = 85

    elif ventas_mensuales >= punto_equilibrio_unidades:
        equilibrio_score = 70

    else:
        equilibrio_score = 25

    # Recuperación de inversión
    if payback_meses is None:
        payback_score = 20

    elif payback_meses <= 12:
        payback_score = 100

    elif payback_meses <= 24:
        payback_score = 85

    elif payback_meses <= 36:
        payback_score = 70

    elif payback_meses <= 60:
        payback_score = 55

    else:
        payback_score = 35

    # --------------------------------------
    # PESOS
    # --------------------------------------

    financial_score = (
        margen_score * 0.25 +
        roi_score * 0.30 +
        equilibrio_score * 0.25 +
        payback_score * 0.20
    )

    # --------------------------------------
    # RESULTADOS
    # --------------------------------------

    print()
    print("==========================================")
    print("          RESULTADOS FINANCIEROS")
    print("==========================================")

    print()

    print(
        f"Ingresos mensuales:       L. {ingresos_mensuales:,.2f}"
    )

    print(
        f"Costos variables:         L. {costos_variables_totales:,.2f}"
    )

    print(
        f"Margen de contribución:   L. {margen_contribucion_total:,.2f}"
    )

    print(
        f"Costos fijos:             L. {costos_fijos:,.2f}"
    )

    print(
        f"Utilidad operativa:       L. {utilidad_operativa:,.2f}"
    )

    print(
        f"Margen operativo:         {margen_operativo * 100:.2f}%"
    )

    print()
    print("------------------------------------------")

    print(
        f"Punto de equilibrio:      "
        f"{punto_equilibrio_unidades:,.0f} unidades"
    )

    print(
        f"Ventas para equilibrio:   "
        f"L. {punto_equilibrio_ventas:,.2f}"
    )

    print()
    print(
        f"Utilidad anual estimada:  "
        f"L. {utilidad_anual:,.2f}"
    )

    print(
        f"ROI anual estimado:       "
        f"{roi_anual * 100:.2f}%"
    )

    if payback_meses is not None:

        print(
            f"Recuperación inversión:   "
            f"{payback_meses:.1f} meses"
        )

    else:

        print(
            "Recuperación inversión:   No recuperable"
        )

    print()
    print("------------------------------------------")

    print(
        f"FINANCIAL SCORE:          "
        f"{financial_score:.2f}/100"
    )

    print("------------------------------------------")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO FINANCIERO")
    print("------------------------------------------")

    if financial_score >= 85:

        print(
            "La estructura financiera presenta condiciones "
            "muy favorables. El negocio muestra buenos márgenes, "
            "retorno y capacidad para superar el punto de equilibrio."
        )

    elif financial_score >= 70:

        print(
            "La estructura financiera es favorable, aunque "
            "existen variables que deben optimizarse antes "
            "de realizar una inversión importante."
        )

    elif financial_score >= 55:

        print(
            "La estructura financiera presenta potencial, "
            "pero requiere ajustes en costos, ventas, margen "
            "o inversión inicial."
        )

    else:

        print(
            "La estructura financiera presenta debilidades "
            "importantes. Se recomienda revisar el modelo "
            "económico antes de continuar."
        )

    return financial_score


def calcular_risk_score():

    print()
    print("==========================================")
    print("             EVALUACIÓN DEL RIESGO")
    print("==========================================")
    print()

    print("Utilice una escala de 0 a 5.")
    print("0 = Riesgo muy bajo")
    print("1 = Riesgo bajo")
    print("2 = Riesgo moderado")
    print("3 = Riesgo medio")
    print("4 = Riesgo alto")
    print("5 = Riesgo muy alto")
    print()

    financiero = float(input(
        "¿Qué tan alto es el riesgo financiero?: "
    ))

    mercado = float(input(
        "¿Qué tan alto es el riesgo de mercado?: "
    ))

    competitivo = float(input(
        "¿Qué tan alto es el riesgo competitivo?: "
    ))

    operativo = float(input(
        "¿Qué tan alto es el riesgo operativo?: "
    ))

    proveedores = float(input(
        "¿Qué tan alta es la dependencia de proveedores?: "
    ))

    clientes = float(input(
        "¿Qué tan alta es la dependencia de clientes?: "
    ))

    regulatorio = float(input(
        "¿Qué tan alto es el riesgo regulatorio?: "
    ))

    # --------------------------------------
    # CONVERTIR RIESGO 0-5 A SCORE 0-100
    # --------------------------------------

    indicadores = {
        "Riesgo financiero": (5 - financiero) * 20,
        "Riesgo de mercado": (5 - mercado) * 20,
        "Riesgo competitivo": (5 - competitivo) * 20,
        "Riesgo operativo": (5 - operativo) * 20,
        "Dependencia de proveedores": (5 - proveedores) * 20,
        "Dependencia de clientes": (5 - clientes) * 20,
        "Riesgo regulatorio": (5 - regulatorio) * 20
    }

    # --------------------------------------
    # PESOS
    # --------------------------------------

    pesos = {
        "Riesgo financiero": 0.25,
        "Riesgo de mercado": 0.20,
        "Riesgo competitivo": 0.15,
        "Riesgo operativo": 0.15,
        "Dependencia de proveedores": 0.10,
        "Dependencia de clientes": 0.10,
        "Riesgo regulatorio": 0.05
    }

    # --------------------------------------
    # CÁLCULO
    # --------------------------------------

    risk_score = 0

    for factor in indicadores:
        risk_score += indicadores[factor] * pesos[factor]

    # --------------------------------------
    # FORTALEZAS Y RIESGOS
    # --------------------------------------

    fortalezas = []
    riesgos = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:
            fortalezas.append(factor)

        elif puntuacion < 60:
            riesgos.append(factor)

    # --------------------------------------
    # RESULTADO
    # --------------------------------------

    print()
    print("==========================================")
    print("             ANÁLISIS DE RIESGO")
    print("==========================================")

    print()

    for factor, puntuacion in indicadores.items():
        print(f"{factor}: {puntuacion:.0f}/100")

    print()
    print("------------------------------------------")
    print(f"RISK SCORE: {risk_score:.2f}/100")
    print("------------------------------------------")

    print()
    print("ÁREAS FAVORABLES")
    print("------------------------------------------")

    if fortalezas:
        for fortaleza in fortalezas:
            print(f"[+] {fortaleza}")
    else:
        print("No se identificaron áreas de riesgo especialmente favorables.")

    print()
    print("PRINCIPALES RIESGOS")
    print("------------------------------------------")

    if riesgos:
        for riesgo in riesgos:
            print(f"[!] {riesgo}")
    else:
        print("No se identificaron riesgos críticos.")

    # --------------------------------------
    # DIAGNÓSTICO
    # --------------------------------------

    print()
    print("DIAGNÓSTICO DE RIESGO")
    print("------------------------------------------")

    if risk_score >= 85:

        print(
            "El proyecto presenta un nivel de riesgo bajo. "
            "Las principales variables muestran condiciones "
            "favorables para operar."
        )

    elif risk_score >= 70:

        print(
            "El proyecto presenta un nivel de riesgo moderado-bajo. "
            "Existen riesgos que deben ser monitoreados."
        )

    elif risk_score >= 55:

        print(
            "El proyecto presenta un nivel de riesgo moderado. "
            "Se recomienda desarrollar estrategias de mitigación "
            "antes de realizar una inversión importante."
        )

    else:

        print(
            "El proyecto presenta un nivel de riesgo elevado. "
            "Se recomienda identificar y reducir los principales "
            "factores de riesgo antes de continuar."
        )

    return risk_score

# ------------------------------------------
# BUSINESS SCORE
# ------------------------------------------

def calcular_business_score(scores):

    pesos = {
        "mercado": 0.20,
        "producto": 0.15,
        "cliente": 0.15,
        "aceptacion": 0.15,
        "competencia": 0.10,
        "posicionamiento": 0.10,
        "finanzas": 0.10,
        "riesgo": 0.05
    }

    score = (
        scores["mercado"] * pesos["mercado"] +
        scores["producto"] * pesos["producto"] +
        scores["cliente"] * pesos["cliente"] +
        scores["aceptacion"] * pesos["aceptacion"] +
        scores["competencia"] * pesos["competencia"] +
        scores["posicionamiento"] * pesos["posicionamiento"] +
        scores["finanzas"] * pesos["finanzas"] +
        scores["riesgo"] * pesos["riesgo"]
    )

    return score


# ------------------------------------------
# RECOMENDACIÓN
# ------------------------------------------

def obtener_recomendacion(score):

    if score >= 85:
        return "ALTA VIABILIDAD"

    elif score >= 70:
        return "VIABLE CON AJUSTES"

    elif score >= 55:
        return "REQUIERE VALIDACIÓN"

    elif score >= 40:
        return "ALTO RIESGO"

    else:
        return "NO RECOMENDADO"


# ------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------

print("==========================================")
print("       BUSINESS VALIDATION MODEL")
print("==========================================")
print()

nombre = input("Nombre del negocio: ")

print()

# ------------------------------------------
# PRODUCTO
# ------------------------------------------


product_score = calcular_product_score()

market_score = calcular_market_score()

customer_score = calcular_customer_score()

acceptance_score = calcular_acceptance_score()

competition_score = calcular_competition_score()

positioning_score = calcular_positioning_score()

financial_score = calcular_financial_score()

risk_score = calcular_risk_score()
print()
print("Ahora introduzca las demás puntuaciones.")


scores = {}

scores["mercado"] = market_score
scores["producto"] = product_score
scores["cliente"] = customer_score
scores["aceptacion"] = acceptance_score
scores["competencia"] = competition_score
scores["posicionamiento"] = positioning_score
scores["finanzas"] = financial_score
scores["riesgo"] = risk_score


# ------------------------------------------
# BUSINESS SCORE
# ------------------------------------------

resultado = analizar_negocio(
    nombre,
    scores
)
guardar_negocio(resultado)

# ------------------------------------------
# RESULTADO
# ------------------------------------------

print()
print("==========================================")
print("                RESULTADO")
print("==========================================")

print()
print(f"Negocio: {nombre}")

print()
print("PUNTUACIONES")
print("------------------------------------------")

print(f"Mercado:             {scores['mercado']:.2f}")
print(f"Producto:            {scores['producto']:.2f}")
print(f"Cliente:             {scores['cliente']:.2f}")
print(f"Aceptación:          {scores['aceptacion']:.2f}")
print(f"Competencia:         {scores['competencia']:.2f}")
print(f"Posicionamiento:     {scores['posicionamiento']:.2f}")
print(f"Finanzas:            {scores['finanzas']:.2f}")
print(f"Riesgo:              {scores['riesgo']:.2f}")

print()
print("------------------------------------------")

print(
    f"BUSINESS SCORE:      "
    f"{resultado['business_score']:.2f}/100"
)

print("------------------------------------------")

print()
print("RECOMENDACIÓN:")
print(resultado["recomendacion"])

print()
print("NIVEL DE RIESGO:")
print(resultado["nivel_riesgo"])

print()
print("DIAGNÓSTICO:")
print("------------------------------------------")
print(resultado["diagnostico"])

print()
print("ALERTAS:")
print("------------------------------------------")

if resultado["alertas"]:

    for alerta in resultado["alertas"]:
        print(f"[!] {alerta}")

else:

    print("No se detectaron alertas críticas.")
print()
print("==========================================")