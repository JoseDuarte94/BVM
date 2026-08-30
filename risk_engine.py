# ==========================================
# BVM RISK ENGINE
# MATRIZ DE RIESGO
# ==========================================


def calcular_risk_score(riesgos):

    resultados = []

    # ======================================
    # CLASIFICACIÓN DEL RIESGO
    # ======================================

    for riesgo in riesgos:

        probabilidad = riesgo["probabilidad"]
        impacto = riesgo["impacto"]

        nivel = probabilidad * impacto

        if nivel >= 21:

            clasificacion = "CRÍTICO"

            accion = (
                "Requiere intervención inmediata y "
                "medidas de mitigación prioritarias."
            )

        elif nivel >= 11:

            clasificacion = "ALTO"

            accion = (
                "Debe establecerse un plan de mitigación "
                "y monitoreo frecuente."
            )

        elif nivel >= 6:

            clasificacion = "MEDIO"

            accion = (
                "Debe ser monitoreado y contar con medidas "
                "preventivas."
            )

        else:

            clasificacion = "BAJO"

            accion = (
                "Mantener monitoreo periódico."
            )

        resultados.append({

            "riesgo":
                riesgo["riesgo"],

            "area":
                riesgo["area"],

            "probabilidad":
                probabilidad,

            "impacto":
                impacto,

            "nivel":
                nivel,

            "clasificacion":
                clasificacion,

            "accion":
                accion
        })

    # ======================================
    # PROMEDIO DE RIESGO
    # ======================================

    if resultados:

        promedio_riesgo = (
            sum(r["nivel"] for r in resultados)
            / len(resultados)
        )

    else:

        promedio_riesgo = 0

    # ======================================
    # CONVERTIR RIESGO A SCORE FAVORABLE
    #
    # 0 riesgo = 100 score
    # 25 riesgo = 0 score
    # ======================================

    risk_score = (
        100 -
        (promedio_riesgo / 25 * 100)
    )

    risk_score = max(
        0,
        min(100, risk_score)
    )

    # ======================================
    # CONTADORES
    # ======================================

    criticos = sum(
        1
        for r in resultados
        if r["clasificacion"] == "CRÍTICO"
    )

    altos = sum(
        1
        for r in resultados
        if r["clasificacion"] == "ALTO"
    )

    medios = sum(
        1
        for r in resultados
        if r["clasificacion"] == "MEDIO"
    )

    bajos = sum(
        1
        for r in resultados
        if r["clasificacion"] == "BAJO"
    )

    # ======================================
    # FORTALEZAS
    # ======================================

    fortalezas = []

    if bajos >= len(resultados) / 2:

        fortalezas.append(
            "La mayoría de los riesgos se encuentran "
            "en niveles bajos."
        )

    if criticos == 0:

        fortalezas.append(
            "No se identificaron riesgos críticos."
        )

    # ======================================
    # DEBILIDADES
    # ======================================

    debilidades = []

    if criticos > 0:

        debilidades.append(
            f"Existen {criticos} riesgo(s) crítico(s)."
        )

    if altos > 0:

        debilidades.append(
            f"Existen {altos} riesgo(s) alto(s)."
        )

    # ======================================
    # ALERTAS
    # ======================================

    alertas = []

    for riesgo in resultados:

        if riesgo["clasificacion"] == "CRÍTICO":

            alertas.append(
                f"Riesgo crítico: {riesgo['riesgo']}"
            )

        elif riesgo["clasificacion"] == "ALTO":

            alertas.append(
                f"Riesgo alto: {riesgo['riesgo']}"
            )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if risk_score >= 85:

        diagnostico = (
            "El proyecto presenta un nivel de riesgo muy bajo. "
            "Las condiciones generales permiten avanzar con "
            "un nivel favorable de exposición."
        )

    elif risk_score >= 70:

        diagnostico = (
            "El proyecto presenta un nivel de riesgo bajo "
            "a moderado. Se recomienda mantener mecanismos "
            "de monitoreo y prevención."
        )

    elif risk_score >= 55:

        diagnostico = (
            "El proyecto presenta un nivel de riesgo moderado. "
            "Se deben implementar medidas de mitigación antes "
            "de realizar una inversión importante."
        )

    elif risk_score >= 40:

        diagnostico = (
            "El proyecto presenta un nivel de riesgo alto. "
            "Existen factores que podrían afectar significativamente "
            "la viabilidad del negocio."
        )

    else:

        diagnostico = (
            "El proyecto presenta un nivel de riesgo crítico. "
            "Se recomienda revisar y modificar la estructura "
            "del proyecto antes de continuar."
        )

    # ======================================
    # NIVEL GENERAL
    # ======================================

    if risk_score >= 85:

        nivel_general = "RIESGO MUY BAJO"

    elif risk_score >= 70:

        nivel_general = "RIESGO BAJO"

    elif risk_score >= 55:

        nivel_general = "RIESGO MODERADO"

    elif risk_score >= 40:

        nivel_general = "RIESGO ALTO"

    else:

        nivel_general = "RIESGO CRÍTICO"

    # ======================================
    # RESULTADO
    # ======================================

    return {

        "risk_score":
            risk_score,

        "nivel_general":
            nivel_general,

        "riesgos":
            resultados,

        "promedio_riesgo":
            promedio_riesgo,

        "criticos":
            criticos,

        "altos":
            altos,

        "medios":
            medios,

        "bajos":
            bajos,

        "indicadores": {

            "Riesgo crítico":
                criticos,

            "Riesgo alto":
                altos,

            "Riesgo medio":
                medios,

            "Riesgo bajo":
                bajos
        },

        "fortalezas":
            fortalezas,

        "debilidades":
            debilidades,

        "alertas":
            alertas,

        "diagnostico":
            diagnostico
    }