import streamlit as st
import plotly.graph_objects as go

from database import obtener_negocios


def mostrar_dashboard():

    st.header("📊 Dashboard BVM")

    # TODO el código que estaba debajo
    # debe quedar dentro de esta función
    st.caption(
        "Panel general de evaluación y desempeño de los proyectos analizados."
    )

    # ======================================
    # OBTENER PROYECTOS
    # ======================================

    negocios = obtener_negocios()

    if not negocios:

        st.info(
            "Todavía no existen proyectos guardados. "
            "Realiza un análisis y guárdalo para comenzar a utilizar el Dashboard."
        )

    else:

        # ==================================
        # CONVERTIR DATOS
        # ==================================

        proyectos = []

        for negocio in negocios:

            proyectos.append({

                "id": negocio[0],
                "nombre": negocio[1],
                "mercado": negocio[2],
                "producto": negocio[3],
                "cliente": negocio[4],
                "aceptacion": negocio[5],
                "competencia": negocio[6],
                "posicionamiento": negocio[7],
                "finanzas": negocio[8],
                "riesgo": negocio[9],
                "business_score": negocio[10],
                "recomendacion": negocio[11],
                "nivel_riesgo": negocio[12],
                "diagnostico": negocio[13]

            })

        # ==================================
        # KPIs PRINCIPALES
        # ==================================

        total_proyectos = len(proyectos)

        promedio_score = (
            sum(
                proyecto["business_score"]
                for proyecto in proyectos
            )
            / total_proyectos
        )

        mejor_proyecto = max(
            proyectos,
            key=lambda x: x["business_score"]
        )

        # ==================================
        # PROYECTO DE MAYOR RIESGO
        # ==================================

        niveles_riesgo = {

            "BAJO": 1,
            "MEDIO": 2,
            "ALTO": 3,
            "CRÍTICO": 4

        }

        proyecto_mayor_riesgo = max(
            proyectos,
            key=lambda x: niveles_riesgo.get(
                str(x["nivel_riesgo"]).upper(),
                0
            )
        )

        # ==================================
        # TARJETAS PRINCIPALES
        # ==================================

        st.subheader("📌 Resumen general")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "📁 Proyectos",
                total_proyectos
            )

        with col2:

            st.metric(
                "📊 Score promedio",
                f"{promedio_score:.2f}/100"
            )

        with col3:

            st.metric(
                "🏆 Mejor proyecto",
                mejor_proyecto["nombre"],
                f"{mejor_proyecto['business_score']:.2f}/100"
            )

        with col4:

            st.metric(
                "⚠️ Mayor riesgo",
                proyecto_mayor_riesgo["nombre"],
                proyecto_mayor_riesgo["nivel_riesgo"]
            )

        st.divider()

        # ==================================
        # SELECCIÓN DE PROYECTO
        # ==================================

        st.subheader("🔎 Análisis visual")

        nombres_proyectos = [
            proyecto["nombre"]
            for proyecto in proyectos
        ]

        proyecto_seleccionado = st.selectbox(
            "Seleccione un proyecto",
            nombres_proyectos
        )

        proyecto = next(
            p for p in proyectos
            if p["nombre"] == proyecto_seleccionado
        )

        # ==================================
        # BUSINESS SCORE
        # ==================================

        st.subheader(
            f"🚀 {proyecto['nombre']}"
        )

        score_col1, score_col2, score_col3 = st.columns(3)

        with score_col1:

            st.metric(
                "BUSINESS SCORE",
                f"{proyecto['business_score']:.2f}/100"
            )

        with score_col2:

            st.write("**Recomendación**")

            st.info(
                proyecto["recomendacion"]
            )

        with score_col3:

            st.write("**Nivel de riesgo**")

            nivel = str(
                proyecto["nivel_riesgo"]
            ).upper()

            if nivel == "CRÍTICO":

                st.error(
                    f"🔴 {nivel}"
                )

            elif nivel == "ALTO":

                st.warning(
                    f"🟠 {nivel}"
                )

            elif nivel == "MEDIO":

                st.warning(
                    f"🟡 {nivel}"
                )

            else:

                st.success(
                    f"🟢 {nivel}"
                )

        st.divider()

        # ==================================
        # DATOS PARA GRÁFICOS
        # ==================================

        indicadores = {

            "Mercado":
                proyecto["mercado"],

            "Producto":
                proyecto["producto"],

            "Cliente":
                proyecto["cliente"],

            "Aceptación":
                proyecto["aceptacion"],

            "Competencia":
                proyecto["competencia"],

            "Posicionamiento":
                proyecto["posicionamiento"],

            "Finanzas":
                proyecto["finanzas"],

            "Riesgo":
                proyecto["riesgo"]

        }

        # ==================================
        # GRÁFICO DE BARRAS
        # ==================================

        st.subheader(
            "📊 Desempeño por áreas"
        )

        figura_barras = go.Figure()

        figura_barras.add_trace(
            go.Bar(

                x=list(
                    indicadores.keys()
                ),

                y=list(
                    indicadores.values()
                ),

                text=[
                    f"{valor:.0f}"
                    for valor in indicadores.values()
                ],

                textposition="outside"

            )
        )

        figura_barras.update_layout(

            yaxis=dict(
                range=[0, 110],
                title="Score"
            ),

            xaxis=dict(
                title=""
            ),

            height=450,

            margin=dict(
                l=40,
                r=40,
                t=30,
                b=80
            ),

            showlegend=False

        )

        st.plotly_chart(
            figura_barras,
            use_container_width=True
        )

        # ==================================
        # RADAR
        # ==================================

        st.subheader(
            "🕸️ Perfil de viabilidad"
        )

        categorias_radar = list(
            indicadores.keys()
        )

        valores_radar = list(
            indicadores.values()
        )

        categorias_radar.append(
            categorias_radar[0]
        )

        valores_radar.append(
            valores_radar[0]
        )

        figura_radar = go.Figure()

        figura_radar.add_trace(

            go.Scatterpolar(

                r=valores_radar,

                theta=categorias_radar,

                fill="toself",

                name=proyecto["nombre"]

            )

        )

        figura_radar.update_layout(

            polar=dict(

                radialaxis=dict(

                    visible=True,

                    range=[
                        0,
                        100
                    ]

                )

            ),

            showlegend=False,

            height=500,

            margin=dict(
                l=60,
                r=60,
                t=30,
                b=30
            )

        )

        st.plotly_chart(
            figura_radar,
            use_container_width=True
        )

        st.divider()

        # ==================================
        # COMPARACIÓN DE PROYECTOS
        # ==================================

        st.subheader(
            "🏆 Comparación de proyectos"
        )

        proyectos_ordenados = sorted(

            proyectos,

            key=lambda x:
                x["business_score"],

            reverse=True

        )

        nombres = [
            proyecto["nombre"]
            for proyecto in proyectos_ordenados
        ]

        scores = [
            proyecto["business_score"]
            for proyecto in proyectos_ordenados
        ]

        figura_comparacion = go.Figure()

        figura_comparacion.add_trace(

            go.Bar(

                x=scores,

                y=nombres,

                orientation="h",

                text=[
                    f"{score:.2f}"
                    for score in scores
                ],

                textposition="outside"

            )

        )

        figura_comparacion.update_layout(

            xaxis=dict(
                range=[0, 110],
                title="Business Score"
            ),

            yaxis=dict(
                title=""
            ),

            height=max(
                350,
                len(proyectos) * 60
            ),

            margin=dict(
                l=120,
                r=50,
                t=30,
                b=50
            ),

            showlegend=False

        )

        st.plotly_chart(

            figura_comparacion,

            use_container_width=True

        )

        st.divider()

        # ==================================
        # DISTRIBUCIÓN DEL RIESGO
        # ==================================

        st.subheader(
            "⚠️ Distribución del riesgo"
        )

        conteo_riesgo = {

            "BAJO": 0,
            "MEDIO": 0,
            "ALTO": 0,
            "CRÍTICO": 0

        }

        for proyecto_item in proyectos:

            nivel = str(
                proyecto_item["nivel_riesgo"]
            ).upper()

            if nivel in conteo_riesgo:

                conteo_riesgo[nivel] += 1

        riesgo_col1, riesgo_col2 = st.columns(2)

        with riesgo_col1:

            figura_riesgo = go.Figure(

                data=[

                    go.Pie(

                        labels=list(
                            conteo_riesgo.keys()
                        ),

                        values=list(
                            conteo_riesgo.values()
                        ),

                        hole=0.45

                    )

                ]

            )

            figura_riesgo.update_layout(

                height=400,

                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )

            )

            st.plotly_chart(

                figura_riesgo,

                use_container_width=True

            )

        with riesgo_col2:

            st.write(
                "### 📋 Resumen de riesgo"
            )

            st.metric(
                "🟢 Bajo",
                conteo_riesgo["BAJO"]
            )

            st.metric(
                "🟡 Medio",
                conteo_riesgo["MEDIO"]
            )

            st.metric(
                "🟠 Alto",
                conteo_riesgo["ALTO"]
            )

            st.metric(
                "🔴 Crítico",
                conteo_riesgo["CRÍTICO"]
            )

        st.divider()

        # ==================================
        # DIAGNÓSTICO
        # ==================================

        st.subheader(
            "🧠 Diagnóstico del proyecto"
        )

        st.info(
            proyecto["diagnostico"]
        )

        # ==================================
        # TABLA RESUMEN
        # ==================================

        st.subheader(
            "📋 Resumen de indicadores"
        )

        resumen_data = {

            "Indicador": list(
                indicadores.keys()
            ),

            "Score": [

                round(
                    valor,
                    2
                )

                for valor
                in indicadores.values()

            ]

        }

        st.dataframe(
            resumen_data,
            use_container_width=True,
            hide_index=True
        )

        # ==========================================
        # RESUMEN EJECUTIVO
        # ==========================================

        st.divider()

        st.subheader("🧠 Resumen ejecutivo")

        # ======================================
        # IDENTIFICAR FORTALEZA Y DEBILIDAD
        # ======================================

        fortaleza = max(
            indicadores,
            key=indicadores.get
        )

        debilidad = min(
            indicadores,
            key=indicadores.get
        )

        score = proyecto["business_score"]

        nivel_riesgo = str(
            proyecto["nivel_riesgo"]
        ).upper()

        # ======================================
        # INTERPRETACIÓN DEL SCORE
        # ======================================

        if score >= 85:

            evaluacion = (
                "El proyecto presenta una **alta viabilidad general** "
                "y muestra condiciones favorables para continuar "
                "con su desarrollo."
            )

        elif score >= 70:

            evaluacion = (
                "El proyecto presenta una **viabilidad favorable**, "
                "aunque existen áreas que deben fortalecerse antes "
                "de realizar una inversión importante."
            )

        elif score >= 55:

            evaluacion = (
                "El proyecto presenta una **viabilidad moderada**. "
                "Se recomienda trabajar en las áreas con menor "
                "puntuación antes de avanzar."
            )

        else:

            evaluacion = (
                "El proyecto presenta **baja viabilidad** bajo "
                "las condiciones evaluadas. Se recomienda revisar "
                "su modelo antes de realizar una inversión."
            )

        # ======================================
        # TARJETAS DEL RESUMEN
        # ======================================

        resumen1, resumen2, resumen3 = st.columns(3)

        with resumen1:

            st.metric(
                "🏆 Business Score",
                f"{score:.2f}/100"
            )

        with resumen2:

            st.metric(
                "💪 Principal fortaleza",
                fortaleza,
                f"{indicadores[fortaleza]:.0f}/100"
            )

        with resumen3:

            st.metric(
                "⚠️ Área a mejorar",
                debilidad,
                f"{indicadores[debilidad]:.0f}/100"
            )

        # ======================================
        # CONCLUSIÓN
        # ======================================

        st.markdown(
            f"""
            ### 📋 Conclusión

            {evaluacion}

            La principal fortaleza identificada es **{fortaleza}**, 
            con una puntuación de **{indicadores[fortaleza]:.0f}/100**.

            El área que requiere mayor atención es **{debilidad}**, 
            con una puntuación de **{indicadores[debilidad]:.0f}/100**.

            El nivel de riesgo registrado para el proyecto es 
            **{nivel_riesgo}**.

            **Recomendación del modelo:**  
            {proyecto["recomendacion"]}
            """
        )

        # ==========================================
        # COMPARACIÓN DE PROYECTOS
        # ==========================================

        st.divider()

        st.subheader("🏆 Comparación de proyectos")

        st.caption(
            "Seleccione los proyectos que desea comparar. "
            "El sistema mostrará su desempeño en los principales indicadores del BVM."
        )

        # ======================================
        # SELECCIÓN DE PROYECTOS
        # ======================================

        proyectos_comparar = st.multiselect(
            "Proyectos a comparar",
            nombres_proyectos,
            default=nombres_proyectos[:2]
        )

        # ======================================
        # VALIDAR SELECCIÓN
        # ======================================

        if len(proyectos_comparar) < 2:

            st.info(
                "Seleccione al menos 2 proyectos para realizar una comparación."
            )

        else:

            proyectos_seleccionados = [

                proyecto_item
                for proyecto_item in proyectos
                if proyecto_item["nombre"] in proyectos_comparar

            ]

            # ==================================
            # BUSINESS SCORE
            # ==================================

            st.write("### 📊 Business Score")

            nombres_comparacion = [
                proyecto_item["nombre"]
                for proyecto_item in proyectos_seleccionados
            ]

            scores_comparacion = [
                proyecto_item["business_score"]
                for proyecto_item in proyectos_seleccionados
            ]

            figura_business = go.Figure()

            figura_business.add_trace(

                go.Bar(

                    x=nombres_comparacion,

                    y=scores_comparacion,

                    text=[
                        f"{score_valor:.2f}"
                        for score_valor in scores_comparacion
                    ],

                    textposition="outside"

                )

            )

            figura_business.update_layout(

                yaxis=dict(
                    range=[0, 110],
                    title="Business Score"
                ),

                xaxis=dict(
                    title=""
                ),

                height=450,

                showlegend=False

            )

            st.plotly_chart(

                figura_business,

                use_container_width=True

            )

            # ==================================
            # COMPARACIÓN POR INDICADORES
            # ==================================

            st.write("### 📈 Comparación por áreas")

            indicadores_comparacion = {

                "Mercado": "mercado",
                "Producto": "producto",
                "Cliente": "cliente",
                "Aceptación": "aceptacion",
                "Competencia": "competencia",
                "Posicionamiento": "posicionamiento",
                "Finanzas": "finanzas",
                "Riesgo": "riesgo"

            }

            figura_comparacion_indicadores = go.Figure()

            for proyecto_item in proyectos_seleccionados:

                valores_comparacion = [

                    proyecto_item[campo]

                    for campo
                    in indicadores_comparacion.values()

                ]

                figura_comparacion_indicadores.add_trace(

                    go.Bar(

                        name=proyecto_item["nombre"],

                        x=list(
                            indicadores_comparacion.keys()
                        ),

                        y=valores_comparacion,

                        text=[
                            f"{valor:.0f}"
                            for valor in valores_comparacion
                        ],

                        textposition="auto"

                    )

                )

            figura_comparacion_indicadores.update_layout(

                barmode="group",

                yaxis=dict(
                    range=[0, 110],
                    title="Score"
                ),

                xaxis=dict(
                    title=""
                ),

                height=500,

                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )

            )

            st.plotly_chart(

                figura_comparacion_indicadores,

                use_container_width=True

            )

            # ==================================
            # TABLA COMPARATIVA
            # ==================================

            st.write("### 📋 Tabla comparativa")

            filas_comparacion = []

            for nombre_indicador, campo in indicadores_comparacion.items():

                fila = [
                    nombre_indicador
                ]

                for proyecto_item in proyectos_seleccionados:

                    fila.append(
                        round(
                            proyecto_item[campo],
                            2
                        )
                    )

                filas_comparacion.append(fila)

            # ==================================
            # BUSINESS SCORE COMO FILA FINAL
            # ==================================

            fila_business = [
                "🚀 Business Score"
            ]

            for proyecto_item in proyectos_seleccionados:

                fila_business.append(
                    round(
                        proyecto_item["business_score"],
                        2
                    )
                )

            filas_comparacion.append(
                fila_business
            )

            datos_comparacion = {

                "Indicador": [
                    fila[0]
                    for fila in filas_comparacion
                ]

            }

            for indice, nombre_columna in enumerate(
                nombres_comparacion
            ):

                datos_comparacion[nombre_columna] = [

                    fila[indice + 1]
                    for fila in filas_comparacion

                ]

            st.dataframe(

                datos_comparacion,

                use_container_width=True,

                hide_index=True

            )

            # ==================================
            # GANADOR
            # ==================================

            mejor_comparacion = max(

                proyectos_seleccionados,

                key=lambda x:
                x["business_score"]

            )

            st.divider()

            st.write(
                "### 🏆 Proyecto con mayor Business Score"
            )

            st.success(

                f"**{mejor_comparacion['nombre']}** "
                f"presenta el mayor Business Score entre "
                f"los proyectos seleccionados: "
                f"**{mejor_comparacion['business_score']:.2f}/100**."

            )