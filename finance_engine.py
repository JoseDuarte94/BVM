# ==========================================
# BVM FINANCE ENGINE
# ==========================================


def calcular_finance_score(datos):

    # ======================================
    # DATOS DE ENTRADA
    # ======================================

    inversion_inicial = float(
        datos.get("inversion_inicial", 0)
    )

    precio_venta = float(
        datos.get("precio_venta", 0)
    )

    unidades_mensuales = float(
        datos.get("unidades_mensuales", 0)
    )

    costo_variable = float(
        datos.get("costo_variable", 0)
    )

    costos_fijos = float(
        datos.get("costos_fijos", 0)
    )


    # ======================================
    # CÁLCULOS FINANCIEROS
    # ======================================

    ingresos_mensuales = (
        precio_venta *
        unidades_mensuales
    )

    costos_variables_mensuales = (
        costo_variable *
        unidades_mensuales
    )

    costo_total_mensual = (
        costos_variables_mensuales +
        costos_fijos
    )

    utilidad_mensual = (
        ingresos_mensuales -
        costo_total_mensual
    )


    # ======================================
    # MARGEN DE CONTRIBUCIÓN
    # ======================================

    margen_contribucion_unitario = (
        precio_venta -
        costo_variable
    )

    if precio_venta > 0:

        margen_contribucion = (
            margen_contribucion_unitario /
            precio_venta
        ) * 100

    else:

        margen_contribucion = 0


    # ======================================
    # PUNTO DE EQUILIBRIO
    # ======================================

    if margen_contribucion_unitario > 0:

        punto_equilibrio_unidades = (
            costos_fijos /
            margen_contribucion_unitario
        )

    else:

        punto_equilibrio_unidades = 0


    punto_equilibrio_ventas = (
        punto_equilibrio_unidades *
        precio_venta
    )


    # ======================================
    # MARGEN DE SEGURIDAD
    # ======================================

    if unidades_mensuales > 0:

        margen_seguridad = (
            (
                unidades_mensuales -
                punto_equilibrio_unidades
            )
            /
            unidades_mensuales
        ) * 100

    else:

        margen_seguridad = 0


    # ======================================
    # ROI MENSUAL
    # ======================================

    if inversion_inicial > 0:

        roi_mensual = (
            utilidad_mensual /
            inversion_inicial
        ) * 100

    else:

        roi_mensual = 0


    # ======================================
    # RECUPERACIÓN DE INVERSIÓN
    # ======================================

    if utilidad_mensual > 0:

        recuperacion_meses = (
            inversion_inicial /
            utilidad_mensual
        )

    else:

        recuperacion_meses = 0


    # ======================================
    # CAPACIDAD DE CUBRIR COSTOS
    # ======================================

    if costo_total_mensual > 0:

        cobertura_costos = (
            ingresos_mensuales /
            costo_total_mensual
        )

    else:

        cobertura_costos = 0


    # ======================================
    # INDICADORES NORMALIZADOS
    # ======================================

    # Margen de contribución
    indicador_margen = max(
        0,
        min(100, margen_contribucion)
    )


    # Margen de seguridad
    indicador_seguridad = max(
        0,
        min(100, margen_seguridad)
    )


    # ROI
    #
    # Se considera:
    # 0% ROI = 0 puntos
    # 20% ROI = 100 puntos
    #
    indicador_roi = max(
        0,
        min(100, roi_mensual * 5)
    )


    # Cobertura de costos
    #
    # 1.00 = ingresos iguales a costos
    # 1.50 = cobertura fuerte
    # 2.00 o más = máximo
    #
    indicador_cobertura = max(
        0,
        min(
            100,
            (cobertura_costos - 1) * 100
        )
    )


    # Utilidad
    #
    # Se evalúa respecto a ingresos.
    #
    if ingresos_mensuales > 0:

        margen_utilidad = (
            utilidad_mensual /
            ingresos_mensuales
        ) * 100

    else:

        margen_utilidad = 0


    indicador_utilidad = max(
        0,
        min(100, margen_utilidad * 5)
    )


    # Punto de equilibrio
    #
    # Mientras menor sea el porcentaje
    # de ventas necesarias para alcanzar
    # el equilibrio, mejor.
    #
    if unidades_mensuales > 0:

        porcentaje_equilibrio = (
            punto_equilibrio_unidades /
            unidades_mensuales
        ) * 100

    else:

        porcentaje_equilibrio = 100


    indicador_equilibrio = max(
        0,
        min(
            100,
            100 - porcentaje_equilibrio
        )
    )


    # ======================================
    # INDICADORES
    # ======================================

    indicadores = {

        "Margen de contribución":
            indicador_margen,

        "Margen de seguridad":
            indicador_seguridad,

        "Rentabilidad sobre inversión":
            indicador_roi,

        "Capacidad de cubrir costos":
            indicador_cobertura,

        "Margen de utilidad":
            indicador_utilidad,

        "Punto de equilibrio":
            indicador_equilibrio
    }


    # ======================================
    # PESOS
    # ======================================

    pesos = {

        "Margen de contribución":
            0.20,

        "Margen de seguridad":
            0.20,

        "Rentabilidad sobre inversión":
            0.20,

        "Capacidad de cubrir costos":
            0.15,

        "Margen de utilidad":
            0.15,

        "Punto de equilibrio":
            0.10
    }


    # ======================================
    # FINANCE SCORE
    # ======================================

    finance_score = 0

    for factor, puntuacion in indicadores.items():

        finance_score += (
            puntuacion *
            pesos[factor]
        )


    finance_score = max(
        0,
        min(100, finance_score)
    )


    # ======================================
    # FORTALEZAS
    # ======================================

    fortalezas = []

    debilidades = []

    for factor, puntuacion in indicadores.items():

        if puntuacion >= 80:

            fortalezas.append(
                factor
            )

        elif puntuacion < 60:

            debilidades.append(
                factor
            )


    # ======================================
    # ALERTAS
    # ======================================

    alertas = []


    if ingresos_mensuales <= 0:

        alertas.append(
            "No existen ingresos mensuales "
            "estimados."
        )


    if utilidad_mensual <= 0:

        alertas.append(
            "El proyecto no genera utilidad "
            "mensual con los datos introducidos."
        )


    if (
        unidades_mensuales > 0
        and
        unidades_mensuales <=
        punto_equilibrio_unidades
    ):

        alertas.append(
            "Las ventas estimadas se encuentran "
            "por debajo o en el punto de equilibrio."
        )


    if margen_contribucion < 30:

        alertas.append(
            "El margen de contribución es reducido."
        )


    if margen_seguridad < 20:

        alertas.append(
            "El margen de seguridad financiero "
            "es bajo."
        )


    if roi_mensual <= 0:

        alertas.append(
            "El retorno sobre la inversión "
            "es insuficiente o negativo."
        )


    if inversion_inicial <= 0:

        alertas.append(
            "No se ha definido una inversión "
            "inicial válida."
        )


    # ======================================
    # DIAGNÓSTICO
    # ======================================

    if finance_score >= 85:

        diagnostico = (
            "El proyecto presenta una estructura "
            "financiera muy favorable. Los ingresos "
            "estimados permiten cubrir los costos, "
            "mantener un margen adecuado y generar "
            "una rentabilidad atractiva."
        )

    elif finance_score >= 70:

        diagnostico = (
            "El proyecto presenta condiciones "
            "financieras favorables. Sin embargo, "
            "algunos indicadores deben ser "
            "monitoreados antes de realizar una "
            "inversión importante."
        )

    elif finance_score >= 55:

        diagnostico = (
            "El proyecto presenta una viabilidad "
            "financiera moderada. Se recomienda "
            "mejorar los márgenes, controlar los "
            "costos o aumentar el volumen de ventas."
        )

    else:

        diagnostico = (
            "El proyecto presenta debilidades "
            "financieras importantes. Se recomienda "
            "revisar precios, costos, volumen de "
            "ventas e inversión inicial antes "
            "de invertir."
        )


    # ======================================
    # RESULTADO FINAL
    # ======================================

    return {

        # Score principal
        "finance_score":
            finance_score,


        # Estructura estándar
        "indicadores":
            indicadores,

        "fortalezas":
            fortalezas,

        "debilidades":
            debilidades,

        "alertas":
            alertas,

        "diagnostico":
            diagnostico,


        # ==================================
        # DATOS FINANCIEROS
        # ==================================

        "inversion_inicial":
            inversion_inicial,

        "precio_venta":
            precio_venta,

        "unidades_mensuales":
            unidades_mensuales,

        "costo_variable":
            costo_variable,

        "costos_fijos":
            costos_fijos,


        # ==================================
        # RESULTADOS CALCULADOS
        # ==================================

        "ingresos_mensuales":
            ingresos_mensuales,

        "costos_variables_mensuales":
            costos_variables_mensuales,

        "costo_total_mensual":
            costo_total_mensual,

        "utilidad_mensual":
            utilidad_mensual,

        "margen_contribucion":
            margen_contribucion,

        "margen_contribucion_unitario":
            margen_contribucion_unitario,

        "punto_equilibrio_unidades":
            punto_equilibrio_unidades,

        "punto_equilibrio_ventas":
            punto_equilibrio_ventas,

        "margen_seguridad":
            margen_seguridad,

        "roi_mensual":
            roi_mensual,

        "recuperacion_meses":
            recuperacion_meses,

        "cobertura_costos":
            cobertura_costos,

        "margen_utilidad":
            margen_utilidad
    }