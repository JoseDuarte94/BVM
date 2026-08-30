# ==========================================
# BVM ENGINE
# ==========================================


# ------------------------------------------
# NIVEL DE RIESGO (a partir del risk_score)
#
# scores["riesgo"] viene de risk_engine y usa
# la convención: 100 = sin riesgo, 0 = riesgo
# máximo. Por eso un risk_score ALTO da un
# nivel de riesgo BAJO.
#
# Usa las mismas 4 etiquetas que ya entiende
# el resto de la app (database.py, app4.py,
# dashboard.py): BAJO, MEDIO, ALTO, CRÍTICO.
# ------------------------------------------

def obtener_nivel_riesgo(risk_score):

    if risk_score >= 75:
        return "BAJO"

    elif risk_score >= 50:
        return "MEDIO"

    elif risk_score >= 25:
        return "ALTO"

    else:
        return "CRÍTICO"


def analizar_negocio(nombre, scores):

    # ======================================
    # PESOS DE LOS ENGINES
    # ======================================

    pesos = {

        "mercado": 0.15,

        "producto": 0.15,

        "cliente": 0.15,

        "aceptacion": 0.10,

        "competencia": 0.10,

        "posicionamiento": 0.10,

        "finanzas": 0.15,

        "riesgo": 0.10
    }


    # ======================================
    # VALIDACIÓN DE DATOS
    # ======================================

    for categoria in pesos:

        if categoria not in scores:

            scores[categoria] = 0

        scores[categoria] = max(
            0,
            min(100, scores[categoria])
        )


    # ======================================
    # CÁLCULO DEL SCORE SIN RIESGO
    # ======================================

    score_base = (

        scores["mercado"] *
        pesos["mercado"]

        +

        scores["producto"] *
        pesos["producto"]

        +

        scores["cliente"] *
        pesos["cliente"]

        +

        scores["aceptacion"] *
        pesos["aceptacion"]

        +

        scores["competencia"] *
        pesos["competencia"]

        +

        scores["posicionamiento"] *
        pesos["posicionamiento"]

        +

        scores["finanzas"] *
        pesos["finanzas"]
    )


    # ======================================
    # CONVERSIÓN DEL RIESGO
    #
    # En Risk Engine:
    #
    # 0  = menor riesgo
    # 100 = mayor riesgo
    #
    # Por eso invertimos el score.
    # ======================================

    riesgo_score = scores["riesgo"]

    riesgo_convertido = 100 - riesgo_score


    # ======================================
    # CONTRIBUCIÓN DEL RIESGO
    # ======================================

    contribucion_riesgo = (

        riesgo_convertido *
        pesos["riesgo"]
    )


    # ======================================
    # BUSINESS SCORE
    # ======================================

    business_score = (

        score_base +
        contribucion_riesgo
    )


    business_score = max(
        0,
        min(100, business_score)
    )


    # ======================================
    # CLASIFICACIÓN
    # ======================================

    if business_score >= 85:

        nivel = "EXCELENTE"

    elif business_score >= 70:

        nivel = "FAVORABLE"

    elif business_score >= 55:

        nivel = "MODERADO"

    elif business_score >= 40:

        nivel = "DÉBIL"

    else:

        nivel = "CRÍTICO"


    # ======================================
    # NIVEL DE RIESGO
    #
    # Distinto de "nivel" (que clasifica el
    # business_score general): esto clasifica
    # específicamente scores["riesgo"], que es
    # lo que usan database.py, app4.py y
    # dashboard.py para mostrar "Nivel de riesgo".
    # ======================================

    nivel_riesgo = obtener_nivel_riesgo(
        scores["riesgo"]
    )


    # ======================================
    # RECOMENDACIÓN
    # ======================================

    if business_score >= 85:

        recomendacion = (

            "El negocio presenta una validación muy favorable. "
            "Existe una combinación sólida de mercado, producto, "
            "cliente y condiciones financieras. Se recomienda "
            "avanzar hacia una etapa de implementación y crecimiento."
        )

    elif business_score >= 70:

        recomendacion = (

            "El negocio presenta condiciones favorables para "
            "continuar desarrollándose. Se recomienda fortalecer "
            "las áreas con menor puntuación antes de realizar "
            "una inversión importante."
        )

    elif business_score >= 55:

        recomendacion = (

            "El negocio presenta una viabilidad moderada. "
            "Se recomienda realizar ajustes en las áreas débiles "
            "y validar nuevamente el modelo antes de escalar."
        )

    elif business_score >= 40:

        recomendacion = (

            "El negocio presenta debilidades importantes. "
            "Se recomienda revisar el modelo de negocio, "
            "especialmente las dimensiones con menor puntuación, "
            "antes de invertir recursos significativos."
        )

    else:

        recomendacion = (

            "El negocio presenta un nivel de validación crítico. "
            "Se recomienda replantear aspectos fundamentales "
            "del modelo antes de proceder con la inversión."
        )


    # ======================================
    # DIAGNÓSTICO
    # ======================================

    categorias_ordenadas = sorted(
        scores.items(),
        key=lambda x: x[1]
    )


    categoria_mas_debil = (
        categorias_ordenadas[0][0]
    )

    categoria_mas_fuerte = (
        categorias_ordenadas[-1][0]
    )


    diagnostico = (

        f"El negocio '{nombre}' presenta un Business Score "
        f"de {business_score:.2f}/100, clasificado como "
        f"{nivel}. "

        f"La dimensión con mejor desempeño es "
        f"'{categoria_mas_fuerte}', mientras que la dimensión "
        f"con menor puntuación es '{categoria_mas_debil}'. "
    )


    # ======================================
    # ALERTAS
    # ======================================

    alertas = []


    if scores["mercado"] < 50:

        alertas.append(
            "El atractivo del mercado presenta una puntuación baja."
        )


    if scores["producto"] < 50:

        alertas.append(
            "El producto presenta debilidades importantes."
        )


    if scores["cliente"] < 50:

        alertas.append(
            "La definición o atractivo del cliente objetivo requiere revisión."
        )


    if scores["aceptacion"] < 50:

        alertas.append(
            "La aceptación del mercado es baja."
        )


    if scores["competencia"] < 50:

        alertas.append(
            "La posición frente a la competencia presenta riesgos."
        )


    if scores["posicionamiento"] < 50:

        alertas.append(
            "El posicionamiento del negocio necesita fortalecerse."
        )


    if scores["finanzas"] < 50:

        alertas.append(
            "La estructura financiera presenta debilidades."
        )


    if scores["riesgo"] >= 70:

        alertas.append(
            "El nivel de riesgo general es elevado."
        )


    # ======================================
    # RESULTADO
    # ======================================

    return {

        "nombre": nombre,

        "business_score": business_score,

        "nivel": nivel,

        "nivel_riesgo": nivel_riesgo,

        "scores": scores,

        "pesos": pesos,

        "riesgo_convertido": riesgo_convertido,

        "recomendacion": recomendacion,

        "diagnostico": diagnostico,

        "alertas": alertas
    }