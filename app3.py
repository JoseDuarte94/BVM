import streamlit as st
import plotly.graph_objects as go

from bvm_engine import analizar_negocio
from market_engine import calcular_market_score
from product_engine import calcular_product_score
from customer_engine import calcular_customer_score
from acceptance_engine import calcular_acceptance_score
from competition_engine import calcular_competition_score
from positioning_engine import calcular_positioning_score
from finance_engine import calcular_finance_score
from risk_engine import calcular_risk_score

from database import (
    inicializar_base_datos,
    guardar_negocio,
    obtener_negocios,
    obtener_riesgos_por_negocio
)


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Business Validation Model",
    page_icon="📊",
    layout="wide"
)

inicializar_base_datos()


# ==========================================
# ESTILO
# ==========================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.score-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.25);
    text-align: center;
}

.score-number {
    font-size: 32px;
    font-weight: bold;
}

.score-label {
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# TÍTULO
# ==========================================

st.title("📊 Business Validation Model")

st.caption(
    "Sistema de análisis y validación de modelos de negocio"
)

st.divider()


# ==========================================
# MENÚ
# ==========================================

st.sidebar.title("BVM")

opcion = st.sidebar.radio(
    "Navegación",
    [
        "Nuevo análisis",
        "Dashboard",
        "Proyectos guardados"
    ]
)

# ==========================================
# FUNCIÓN PARA MOSTRAR RESULTADOS DE ENGINE
# ==========================================

def mostrar_resultado_engine(
    resultado,
    score_key,
    titulo
):

    st.subheader(titulo)

    # ======================================
    # SCORE
    # ======================================

    st.metric(
        "SCORE",
        f"{resultado[score_key]:.2f}/100"
    )

    # ======================================
    # INDICADORES
    # ======================================

    st.subheader("📋 Indicadores")

    for factor, valor in resultado["indicadores"].items():

        st.write(
            f"**{factor}:** {valor:.0f}/100"
        )

    # ======================================
    # FORTALEZAS Y DEBILIDADES
    # ======================================

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 💪 Fortalezas")

        if resultado["fortalezas"]:

            for item in resultado["fortalezas"]:

                st.success(item)

        else:

            st.write(
                "No se identificaron fortalezas."
            )

    with col2:

        st.write("### ⚠️ Debilidades")

        if resultado["debilidades"]:

            for item in resultado["debilidades"]:

                st.warning(item)

        else:

            st.write(
                "No se identificaron debilidades."
            )

    # ======================================
    # DIAGNÓSTICO
    # ======================================

    st.write("### 🧠 Diagnóstico")

    st.info(
        resultado["diagnostico"]
    )

    # ======================================
    # ALERTAS
    # ======================================

    if resultado["alertas"]:

        st.write("### 🚨 Alertas")

        for alerta in resultado["alertas"]:

            st.warning(alerta)

    else:

        st.success(
            "No se detectaron alertas."
        )

# ==========================================
# NUEVO ANÁLISIS
# ==========================================

if opcion == "Nuevo análisis":
    st.header("🚀 Nuevo análisis")

    PASOS = [
        "🌎 Mercado",
        "📦 Producto",
        "👤 Cliente",
        "❤️ Aceptación",
        "⚔️ Competencia",
        "🎯 Posicionamiento",
        "💰 Finanzas",
        "🚨 Riesgo",
        "✅ Resumen"
    ]

    if "paso_actual" not in st.session_state:
        st.session_state.paso_actual = 0

    if "lista_riesgos" not in st.session_state:
        st.session_state.lista_riesgos = []

    paso = st.session_state.paso_actual

    # ======================================
    # NOMBRE DEL NEGOCIO (SIEMPRE VISIBLE)
    # ======================================

    nombre = st.text_input(
        "Nombre del negocio",
        key="nombre_negocio",
        placeholder="Ej. Casa Lenca"
    )

    # ======================================
    # INDICADOR DE PROGRESO
    # ======================================

    st.progress(paso / (len(PASOS) - 1))

    st.caption(
        f"Paso {paso + 1} de {len(PASOS)}: {PASOS[paso]}"
    )

    st.divider()

    # ======================================
    # PASO 0: MERCADO
    # ======================================

    if paso == 0:

        st.subheader("🌎 Análisis del mercado")

        poblacion = st.number_input(
            "Población del área de mercado",
            min_value=0,
            value=25000,
            step=100,
            key="poblacion"
        )

        porcentaje_objetivo = st.number_input(
            "Porcentaje estimado del mercado objetivo (%)",
            min_value=0.0,
            max_value=100.0,
            value=35.0,
            step=1.0,
            key="porcentaje_objetivo"
        )

        frecuencia_compra = st.number_input(
            "Frecuencia promedio de compra mensual",
            min_value=0.0,
            value=2.5,
            step=0.1,
            key="frecuencia_compra"
        )

        ventas_estimadas = st.number_input(
            "Unidades vendidas estimadas mensualmente",
            min_value=0,
            value=15000,
            step=100,
            key="ventas_estimadas"
        )

        crecimiento = st.number_input(
            "Crecimiento estimado del mercado (%)",
            min_value=-100.0,
            value=6.0,
            step=0.5,
            key="crecimiento"
        )

        accesibilidad = st.slider(
            "Accesibilidad al mercado",
            0,
            100,
            80,
            key="accesibilidad_mercado"
        )

        datos_mercado = {
            "poblacion": poblacion,
            "porcentaje_objetivo": porcentaje_objetivo,
            "frecuencia_compra": frecuencia_compra,
            "ventas_estimadas": ventas_estimadas,
            "crecimiento": crecimiento,
            "accesibilidad": accesibilidad
        }

        resultado_mercado = calcular_market_score(datos_mercado)

        st.divider()

        st.write("#### 📊 Vista previa")

        mercado_col1, mercado_col2, mercado_col3 = st.columns(3)

        with mercado_col1:
            st.metric(
                "Mercado objetivo",
                f"{resultado_mercado['mercado_objetivo']:,.0f}"
            )

        with mercado_col2:
            st.metric(
                "Demanda potencial",
                f"{resultado_mercado['demanda_potencial']:,.0f}"
            )

        with mercado_col3:
            st.metric(
                "Cobertura",
                f"{resultado_mercado['cobertura']:.2f}%"
            )

        st.metric(
            "MARKET SCORE",
            f"{resultado_mercado['market_score']:.2f}/100"
        )

    # ======================================
    # PASO 1: PRODUCTO
    # ======================================

    elif paso == 1:

        st.subheader("📦 Análisis del producto")

        necesidad = st.slider("Necesidad que resuelve", 0, 100, 50, key="necesidad_producto")
        valor_percibido = st.slider("Valor percibido", 0, 100, 50, key="valor_percibido")
        diferenciacion = st.slider("Diferenciación", 0, 100, 50, key="diferenciacion_producto")
        calidad = st.slider("Calidad esperada", 0, 100, 50, key="calidad")
        innovacion = st.slider("Innovación", 0, 100, 50, key="innovacion")
        sustitucion = st.slider("Dificultad de sustitución", 0, 100, 50, key="sustitucion")

        datos_producto = {
            "necesidad": necesidad,
            "valor_percibido": valor_percibido,
            "diferenciacion": diferenciacion,
            "calidad": calidad,
            "innovacion": innovacion,
            "sustitucion": sustitucion
        }

        resultado_producto = calcular_product_score(datos_producto)

        st.divider()

        mostrar_resultado_engine(
            resultado_producto,
            "product_score",
            "📊 Vista previa"
        )

    # ======================================
    # PASO 2: CLIENTE
    # ======================================

    elif paso == 2:

        st.subheader("👤 Análisis del cliente")

        definicion_cliente = st.slider("Claridad en la definición del cliente", 0, 100, 50, key="definicion_cliente")
        necesidad_cliente = st.slider("Necesidad del cliente", 0, 100, 50, key="necesidad_cliente")
        capacidad_pago = st.slider("Capacidad de pago", 0, 100, 50, key="capacidad_pago")
        accesibilidad_cliente = st.slider("Accesibilidad al cliente", 0, 100, 50, key="accesibilidad_cliente")
        frecuencia_cliente = st.slider("Frecuencia potencial de compra", 0, 100, 50, key="frecuencia_cliente")
        tamano_segmento = st.slider("Tamaño del segmento", 0, 100, 50, key="tamano_segmento")

        datos_cliente = {
            "definicion_cliente": definicion_cliente,
            "necesidad": necesidad_cliente,
            "capacidad_pago": capacidad_pago,
            "accesibilidad": accesibilidad_cliente,
            "frecuencia": frecuencia_cliente,
            "tamano_segmento": tamano_segmento
        }

        resultado_cliente = calcular_customer_score(datos_cliente)

        st.divider()

        mostrar_resultado_engine(
            resultado_cliente,
            "customer_score",
            "📊 Vista previa"
        )

    # ======================================
    # PASO 3: ACEPTACIÓN
    # ======================================

    elif paso == 3:

        st.subheader("❤️ Análisis de aceptación")

        intencion = st.slider("Intención de compra", 0, 100, 50, key="intencion")
        relevancia = st.slider("Relevancia del producto", 0, 100, 50, key="relevancia")
        disposicion_pago = st.slider("Disposición a pagar", 0, 100, 50, key="disposicion_pago")
        confianza = st.slider("Confianza en el producto o marca", 0, 100, 50, key="confianza")
        facilidad_compra = st.slider("Facilidad de compra", 0, 100, 50, key="facilidad_compra")
        barreras = st.slider("Bajas barreras de compra", 0, 100, 50, key="barreras_aceptacion")

        datos_aceptacion = {
            "intencion": intencion,
            "relevancia": relevancia,
            "disposicion_pago": disposicion_pago,
            "confianza": confianza,
            "facilidad_compra": facilidad_compra,
            "barreras": barreras
        }

        resultado_aceptacion = calcular_acceptance_score(datos_aceptacion)

        st.divider()

        mostrar_resultado_engine(
            resultado_aceptacion,
            "acceptance_score",
            "📊 Vista previa"
        )

    # ======================================
    # PASO 4: COMPETENCIA
    # ======================================

    elif paso == 4:

        st.subheader("⚔️ Análisis de la competencia")

        competencia_directa = st.slider(
            "Fortaleza frente a competidores directos", 0, 100, 50, key="competencia_directa"
        )
        cantidad_competidores = st.slider(
            "Facilidad para competir frente a la cantidad de competidores", 0, 100, 50, key="cantidad_competidores"
        )
        intensidad = st.slider("Intensidad competitiva favorable", 0, 100, 50, key="intensidad_competitiva")
        ventajas_competidores = st.slider(
            "Capacidad para enfrentar las ventajas de los competidores", 0, 100, 50, key="ventajas_competidores"
        )
        barreras_entrada = st.slider("Barreras de entrada del mercado", 0, 100, 50, key="barreras_entrada")
        diferenciacion_competencia = st.slider(
            "Diferenciación frente a competidores", 0, 100, 50, key="diferenciacion_competencia"
        )

        datos_competencia = {
            "competencia_directa": competencia_directa,
            "cantidad_competidores": cantidad_competidores,
            "intensidad": intensidad,
            "ventajas_competidores": ventajas_competidores,
            "barreras_entrada": barreras_entrada,
            "diferenciacion": diferenciacion_competencia
        }

        resultado_competencia = calcular_competition_score(datos_competencia)

        st.divider()

        mostrar_resultado_engine(
            resultado_competencia,
            "competition_score",
            "📊 Vista previa"
        )

    # ======================================
    # PASO 5: POSICIONAMIENTO
    # ======================================

    elif paso == 5:

        st.subheader("🎯 Análisis del posicionamiento")

        claridad_marca = st.slider("Claridad de la marca", 0, 100, 50, key="claridad_marca")
        propuesta_valor = st.slider("Claridad de la propuesta de valor", 0, 100, 50, key="propuesta_valor")
        diferenciacion_posicionamiento = st.slider(
            "Diferenciación frente al mercado", 0, 100, 50, key="diferenciacion_posicionamiento"
        )
        posicionamiento_precio = st.slider(
            "Adecuación del posicionamiento de precio", 0, 100, 50, key="posicionamiento_precio"
        )
        reconocimiento = st.slider("Reconocimiento de marca", 0, 100, 50, key="reconocimiento")
        coherencia = st.slider(
            "Coherencia entre marca, producto y mercado", 0, 100, 50, key="coherencia"
        )

        datos_posicionamiento = {
            "claridad_marca": claridad_marca,
            "propuesta_valor": propuesta_valor,
            "diferenciacion": diferenciacion_posicionamiento,
            "posicionamiento_precio": posicionamiento_precio,
            "reconocimiento": reconocimiento,
            "coherencia": coherencia
        }

        resultado_posicionamiento = calcular_positioning_score(datos_posicionamiento)

        st.divider()

        mostrar_resultado_engine(
            resultado_posicionamiento,
            "positioning_score",
            "📊 Vista previa"
        )

    # ======================================
    # PASO 6: FINANZAS
    # ======================================

    elif paso == 6:

        st.subheader("💰 Análisis financiero")

        inversion_inicial = st.number_input(
            "Inversión inicial (L)", min_value=0.0, value=0.0, step=1000.0, key="inversion_inicial"
        )
        precio_venta = st.number_input(
            "Precio promedio de venta por unidad (L)", min_value=0.0, value=0.0, step=1.0, key="precio_venta"
        )
        unidades_mensuales = st.number_input(
            "Unidades vendidas mensualmente", min_value=0, value=0, step=100, key="unidades_mensuales"
        )
        costo_variable = st.number_input(
            "Costo variable por unidad (L)", min_value=0.0, value=0.0, step=0.50, key="costo_variable"
        )
        costos_fijos = st.number_input(
            "Costos fijos mensuales (L)", min_value=0.0, value=0.0, step=1000.0, key="costos_fijos"
        )

        datos_finanzas = {
            "inversion_inicial": inversion_inicial,
            "precio_venta": precio_venta,
            "unidades_mensuales": unidades_mensuales,
            "costo_variable": costo_variable,
            "costos_fijos": costos_fijos
        }

        resultado_finanzas = calcular_finance_score(datos_finanzas)

        st.divider()

        mostrar_resultado_engine(
            resultado_finanzas,
            "finance_score",
            "📊 Vista previa"
        )

        st.write("#### 💵 Resumen financiero")

        fin_col1, fin_col2, fin_col3 = st.columns(3)

        with fin_col1:
            st.metric("Ingresos mensuales", f"L {resultado_finanzas['ingresos_mensuales']:,.2f}")

        with fin_col2:
            st.metric("Costos mensuales", f"L {resultado_finanzas['costo_total_mensual']:,.2f}")

        with fin_col3:
            st.metric("Utilidad mensual", f"L {resultado_finanzas['utilidad_mensual']:,.2f}")

        fin_col4, fin_col5, fin_col6 = st.columns(3)

        with fin_col4:
            st.metric(
                "Punto de equilibrio",
                f"{resultado_finanzas['punto_equilibrio_unidades']:,.0f} unidades"
            )

        with fin_col5:
            st.metric("ROI mensual", f"{resultado_finanzas['roi_mensual']:.2f}%")

        with fin_col6:
            st.metric(
                "Recuperación",
                (
                    f"{resultado_finanzas['recuperacion_meses']:.1f} meses"
                    if resultado_finanzas["recuperacion_meses"] > 0
                    else "No recuperable"
                )
            )

    # ======================================
    # PASO 7: RIESGO
    # ======================================

    elif paso == 7:

        st.subheader("📊 Matriz de riesgos")

        st.caption("Nivel de riesgo = Probabilidad × Impacto")

        etiquetas_probabilidad = {
            1: "1 - Muy baja",
            2: "2 - Baja",
            3: "3 - Media",
            4: "4 - Alta",
            5: "5 - Muy alta"
        }

        etiquetas_impacto = {
            1: "1 - Muy bajo",
            2: "2 - Bajo",
            3: "3 - Medio",
            4: "4 - Alto",
            5: "5 - Muy alto"
        }

        riesgo_col1, riesgo_col2 = st.columns(2)

        with riesgo_col1:
            nombre_riesgo = st.text_input(
                "Nombre del riesgo", placeholder="Ej. Riesgo cambiario", key="nombre_riesgo_input"
            )

        with riesgo_col2:
            area_riesgo = st.selectbox(
                "Área asociada",
                [
                    "Mercado", "Producto", "Cliente", "Competencia",
                    "Posicionamiento", "Finanzas", "Operación", "Legal", "Otro"
                ],
                key="area_riesgo_input"
            )

        riesgo_col3, riesgo_col4 = st.columns(2)

        with riesgo_col3:
            probabilidad_riesgo = st.select_slider(
                "Probabilidad de ocurrencia",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: etiquetas_probabilidad[x],
                key="probabilidad_riesgo_input"
            )

        with riesgo_col4:
            impacto_riesgo = st.select_slider(
                "Impacto si ocurre",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: etiquetas_impacto[x],
                key="impacto_riesgo_input"
            )

        nivel_riesgo = probabilidad_riesgo * impacto_riesgo

        def clasificar_nivel_riesgo(nivel):
            if nivel <= 5:
                return "BAJO", "🟢"
            elif nivel <= 10:
                return "MEDIO", "🟡"
            elif nivel <= 15:
                return "ALTO", "🟠"
            else:
                return "CRÍTICO", "🔴"

        categoria_riesgo, emoji_riesgo = clasificar_nivel_riesgo(nivel_riesgo)

        probabilidades = [5, 4, 3, 2, 1]
        impactos = [1, 2, 3, 4, 5]

        z_valores = [[p * i for i in impactos] for p in probabilidades]
        z_base = [[0 for _ in impactos] for _ in probabilidades]

        z_resaltado = [[None for _ in impactos] for _ in probabilidades]
        texto_resaltado = [["" for _ in impactos] for _ in probabilidades]

        fila_sel = probabilidades.index(probabilidad_riesgo)
        columna_sel = impactos.index(impacto_riesgo)

        z_resaltado[fila_sel][columna_sel] = nivel_riesgo
        texto_resaltado[fila_sel][columna_sel] = str(nivel_riesgo)

        figura_riesgo = go.Figure()

        figura_riesgo.add_trace(
            go.Heatmap(
                z=z_base,
                x=impactos,
                y=probabilidades,
                text=z_valores,
                texttemplate="%{text}",
                textfont={"size": 16, "color": "#9ca3af"},
                colorscale=[[0.0, "#f3f4f6"], [1.0, "#f3f4f6"]],
                zmin=0,
                zmax=0,
                showscale=False,
                hoverinfo="skip"
            )
        )

        figura_riesgo.add_trace(
            go.Heatmap(
                z=z_resaltado,
                x=impactos,
                y=probabilidades,
                text=texto_resaltado,
                texttemplate="%{text}",
                textfont={"size": 22, "color": "white"},
                colorscale=[
                    [0.00, "#27ae60"], [0.20, "#27ae60"],
                    [0.21, "#f1c40f"], [0.40, "#f1c40f"],
                    [0.41, "#e67e22"], [0.60, "#e67e22"],
                    [0.61, "#e74c3c"], [1.00, "#e74c3c"]
                ],
                zmin=1,
                zmax=25,
                showscale=False,
                hovertemplate="Probabilidad: %{y}<br>Impacto: %{x}<br>Nivel: %{z}<extra></extra>"
            )
        )

        figura_riesgo.update_layout(
            title={"text": "MATRIZ DE RIESGO", "x": 0.5, "xanchor": "center"},
            xaxis=dict(
                title="Impacto",
                tickmode="array",
                tickvals=impactos,
                ticktext=["1 - Muy bajo", "2 - Bajo", "3 - Medio", "4 - Alto", "5 - Muy alto"]
            ),
            yaxis=dict(
                title="Probabilidad",
                tickmode="array",
                tickvals=probabilidades,
                ticktext=["5 - Muy alta", "4 - Alta", "3 - Media", "2 - Baja", "1 - Muy baja"]
            ),
            height=550,
            margin=dict(l=80, r=30, t=80, b=80)
        )

        st.plotly_chart(figura_riesgo, use_container_width=True)

        mensaje_resumen = (
            f"{emoji_riesgo} Con una probabilidad **{etiquetas_probabilidad[probabilidad_riesgo]}** "
            f"y un impacto **{etiquetas_impacto[impacto_riesgo]}**, el nivel de riesgo calculado es "
            f"**{nivel_riesgo}**, clasificado como **{categoria_riesgo}**."
        )

        if categoria_riesgo == "BAJO":
            st.success(mensaje_resumen)
        elif categoria_riesgo == "MEDIO":
            st.warning(mensaje_resumen)
        elif categoria_riesgo == "ALTO":
            st.info(mensaje_resumen)
        else:
            st.error(mensaje_resumen)

        if st.button("➕ Agregar riesgo a la lista"):
            if not nombre_riesgo:
                st.warning("Debe ingresar un nombre para el riesgo antes de agregarlo.")
            else:
                st.session_state.lista_riesgos.append({
                    "riesgo": nombre_riesgo,
                    "area": area_riesgo,
                    "probabilidad": probabilidad_riesgo,
                    "impacto": impacto_riesgo
                })
                st.success(f"Riesgo '{nombre_riesgo}' agregado a la lista.")
                st.rerun()

        st.write("### 📋 Riesgos registrados")

        if st.session_state.lista_riesgos:

            for indice, riesgo_item in enumerate(st.session_state.lista_riesgos):

                nivel_item = riesgo_item["probabilidad"] * riesgo_item["impacto"]

                tabla_col1, tabla_col2, tabla_col3, tabla_col4, tabla_col5 = st.columns([3, 2, 2, 2, 1])

                with tabla_col1:
                    st.write(f"**{riesgo_item['riesgo']}**")
                with tabla_col2:
                    st.write(riesgo_item["area"])
                with tabla_col3:
                    st.write(f"P: {riesgo_item['probabilidad']} · I: {riesgo_item['impacto']}")
                with tabla_col4:
                    st.write(f"Nivel: {nivel_item}")
                with tabla_col5:
                    if st.button("🗑️", key=f"eliminar_riesgo_{indice}"):
                        st.session_state.lista_riesgos.pop(indice)
                        st.rerun()

            if st.button("🗑️ Vaciar lista de riesgos"):
                st.session_state.lista_riesgos = []
                st.rerun()

        else:

            st.info(
                "Todavía no has agregado riesgos a la lista. Completa el "
                "formulario de arriba y presiona '➕ Agregar riesgo a la lista'."
            )

        st.divider()

        mostrar_resultado_engine(
            calcular_risk_score(st.session_state.lista_riesgos),
            "risk_score",
            "📊 Vista previa: riesgo general"
        )

    # ======================================
    # PASO 8: RESUMEN
    # ======================================

    elif paso == 8:

        st.subheader("✅ Resumen y análisis final")

        if not nombre:
            st.warning("Debe ingresar el nombre del negocio (arriba) antes de guardar.")

        datos_mercado = {
            "poblacion": st.session_state.get("poblacion", 0),
            "porcentaje_objetivo": st.session_state.get("porcentaje_objetivo", 0.0),
            "frecuencia_compra": st.session_state.get("frecuencia_compra", 0.0),
            "ventas_estimadas": st.session_state.get("ventas_estimadas", 0),
            "crecimiento": st.session_state.get("crecimiento", 0.0),
            "accesibilidad": st.session_state.get("accesibilidad_mercado", 0)
        }

        datos_producto = {
            "necesidad": st.session_state.get("necesidad_producto", 0),
            "valor_percibido": st.session_state.get("valor_percibido", 0),
            "diferenciacion": st.session_state.get("diferenciacion_producto", 0),
            "calidad": st.session_state.get("calidad", 0),
            "innovacion": st.session_state.get("innovacion", 0),
            "sustitucion": st.session_state.get("sustitucion", 0)
        }

        datos_cliente = {
            "definicion_cliente": st.session_state.get("definicion_cliente", 0),
            "necesidad": st.session_state.get("necesidad_cliente", 0),
            "capacidad_pago": st.session_state.get("capacidad_pago", 0),
            "accesibilidad": st.session_state.get("accesibilidad_cliente", 0),
            "frecuencia": st.session_state.get("frecuencia_cliente", 0),
            "tamano_segmento": st.session_state.get("tamano_segmento", 0)
        }

        datos_aceptacion = {
            "intencion": st.session_state.get("intencion", 0),
            "relevancia": st.session_state.get("relevancia", 0),
            "disposicion_pago": st.session_state.get("disposicion_pago", 0),
            "confianza": st.session_state.get("confianza", 0),
            "facilidad_compra": st.session_state.get("facilidad_compra", 0),
            "barreras": st.session_state.get("barreras_aceptacion", 0)
        }

        datos_competencia = {
            "competencia_directa": st.session_state.get("competencia_directa", 0),
            "cantidad_competidores": st.session_state.get("cantidad_competidores", 0),
            "intensidad": st.session_state.get("intensidad_competitiva", 0),
            "ventajas_competidores": st.session_state.get("ventajas_competidores", 0),
            "barreras_entrada": st.session_state.get("barreras_entrada", 0),
            "diferenciacion": st.session_state.get("diferenciacion_competencia", 0)
        }

        datos_posicionamiento = {
            "claridad_marca": st.session_state.get("claridad_marca", 0),
            "propuesta_valor": st.session_state.get("propuesta_valor", 0),
            "diferenciacion": st.session_state.get("diferenciacion_posicionamiento", 0),
            "posicionamiento_precio": st.session_state.get("posicionamiento_precio", 0),
            "reconocimiento": st.session_state.get("reconocimiento", 0),
            "coherencia": st.session_state.get("coherencia", 0)
        }

        datos_finanzas = {
            "inversion_inicial": st.session_state.get("inversion_inicial", 0.0),
            "precio_venta": st.session_state.get("precio_venta", 0.0),
            "unidades_mensuales": st.session_state.get("unidades_mensuales", 0),
            "costo_variable": st.session_state.get("costo_variable", 0.0),
            "costos_fijos": st.session_state.get("costos_fijos", 0.0)
        }

        resultado_mercado = calcular_market_score(datos_mercado)
        resultado_producto = calcular_product_score(datos_producto)
        resultado_cliente = calcular_customer_score(datos_cliente)
        resultado_aceptacion = calcular_acceptance_score(datos_aceptacion)
        resultado_competencia = calcular_competition_score(datos_competencia)
        resultado_posicionamiento = calcular_positioning_score(datos_posicionamiento)
        resultado_finanzas = calcular_finance_score(datos_finanzas)
        resultado_riesgo = calcular_risk_score(st.session_state.lista_riesgos)

        scores = {
            "mercado": resultado_mercado["market_score"],
            "producto": resultado_producto["product_score"],
            "cliente": resultado_cliente["customer_score"],
            "aceptacion": resultado_aceptacion["acceptance_score"],
            "competencia": resultado_competencia["competition_score"],
            "posicionamiento": resultado_posicionamiento["positioning_score"],
            "finanzas": resultado_finanzas["finance_score"],
            "riesgo": resultado_riesgo["risk_score"]
        }

        nombres_categorias = {
            "mercado": "Mercado",
            "producto": "Producto",
            "cliente": "Cliente",
            "aceptacion": "Aceptación",
            "competencia": "Competencia",
            "posicionamiento": "Posicionamiento",
            "finanzas": "Finanzas",
            "riesgo": "Riesgo"
        }

        st.write("#### 📊 Vista previa de resultados")

        score_cols = st.columns(4)

        for i, categoria in enumerate(scores):
            with score_cols[i % 4]:
                st.metric(nombres_categorias[categoria], f"{scores[categoria]:.0f}/100")

        st.write("#### 🎯 Perfil del negocio")

        categorias_radar = [nombres_categorias[c] for c in scores]
        valores_radar = list(scores.values())

        categorias_radar = categorias_radar + [categorias_radar[0]]
        valores_radar = valores_radar + [valores_radar[0]]

        figura = go.Figure()

        figura.add_trace(
            go.Scatterpolar(
                r=valores_radar,
                theta=categorias_radar,
                fill="toself",
                name=nombre or "Negocio"
            )
        )

        figura.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True
        )

        st.plotly_chart(figura, use_container_width=True)

        st.divider()

        if st.button(
            "🚀 Analizar y guardar",
            type="primary",
            use_container_width=True,
            disabled=not nombre
        ):

            resultado = analizar_negocio(nombre, scores)

            guardar_negocio(resultado, resultado_riesgo["riesgos"])

            st.success(
                "Análisis completado y guardado correctamente. Puedes verlo en el Dashboard."
            )

            st.subheader("📊 Resultado del análisis")

            resultado_col1, resultado_col2 = st.columns(2)

            with resultado_col1:
                st.metric("BUSINESS SCORE", f"{resultado['business_score']:.2f}/100")

            with resultado_col2:
                st.metric("Nivel de riesgo general", resultado["nivel_riesgo"])

            st.write(f"**Recomendación:** {resultado['recomendacion']}")

            st.write("#### 🧠 Diagnóstico")
            st.write(resultado["diagnostico"])

            if resultado["alertas"]:
                st.write("#### ⚠️ Alertas")
                for alerta in resultado["alertas"]:
                    st.warning(alerta)
            else:
                st.success("No se detectaron alertas críticas.")

            if st.button("🔄 Empezar un nuevo análisis"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

    # ======================================
    # NAVEGACIÓN ENTRE PASOS
    # ======================================

    st.divider()

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        if paso > 0:
            if st.button("⬅️ Anterior", use_container_width=True):
                st.session_state.paso_actual -= 1
                st.rerun()

    with nav_col2:
        if paso < len(PASOS) - 1:
            if st.button("Siguiente ➡️", use_container_width=True):
                st.session_state.paso_actual += 1
                st.rerun()

# ==========================================
# DASHBOARD
# ==========================================

elif opcion == "Dashboard":

    st.header("📊 Dashboard general")

    negocios = obtener_negocios()


    if not negocios:

        st.info(
            "Todavía no existen proyectos analizados."
        )

    else:

        scores = [
            negocio[2]
            for negocio in negocios
        ]


        promedio = sum(scores) / len(scores)


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Proyectos analizados",
                len(negocios)
            )


        with col2:

            st.metric(
                "Score promedio",
                f"{promedio:.2f}"
            )


        with col3:

            st.metric(
                "Mejor score",
                f"{max(scores):.2f}"
            )


        st.divider()


        st.subheader(
            "🏆 Proyectos"
        )


        for negocio in negocios:

            id_negocio = negocio[0]
            nombre = negocio[1]
            score = negocio[2]
            recomendacion = negocio[3]
            riesgo = negocio[4]


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.write(
                    f"**{nombre}**"
                )


            with col2:

                st.metric(
                    "Score",
                    f"{score:.2f}"
                )


            with col3:

                st.write(
                    recomendacion
                )


            with col4:

                st.write(
                    riesgo
                )


            st.divider()


# ==========================================
# PROYECTOS GUARDADOS
# ==========================================

elif opcion == "Proyectos guardados":

    st.header("📁 Proyectos guardados")

    negocios = obtener_negocios()


    if not negocios:

        st.info(
            "No existen proyectos guardados."
        )

    else:

        for negocio in negocios:

            id_negocio = negocio[0]
            nombre = negocio[1]
            score = negocio[2]
            recomendacion = negocio[3]
            riesgo = negocio[4]


            with st.expander(
                f"{nombre} — {score:.2f}/100"
            ):

                st.write(
                    f"**ID:** {id_negocio}"
                )

                st.write(
                    f"**Business Score:** {score:.2f}/100"
                )

                st.write(
                    f"**Recomendación:** {recomendacion}"
                )

                st.write(
                    f"**Nivel de riesgo:** {riesgo}"
                )

                # ==========================
                # DETALLE DE RIESGOS
                # ==========================

                riesgos_negocio = obtener_riesgos_por_negocio(
                    id_negocio
                )

                if riesgos_negocio:

                    st.write("**Riesgos identificados:**")

                    for riesgo_detalle in riesgos_negocio:

                        nombre_r = riesgo_detalle[0]
                        area_r = riesgo_detalle[1]
                        probabilidad_r = riesgo_detalle[2]
                        impacto_r = riesgo_detalle[3]
                        nivel_r = riesgo_detalle[4]
                        clasificacion_r = riesgo_detalle[5]

                        st.write(
                            f"- **{nombre_r}** ({area_r}) — "
                            f"P: {probabilidad_r} · I: {impacto_r} · "
                            f"Nivel: {nivel_r} · {clasificacion_r}"
                        )

                else:

                    st.caption(
                        "No se registraron riesgos individuales "
                        "para este proyecto."
                    )