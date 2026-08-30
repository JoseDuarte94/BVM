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
    obtener_negocios
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

    nombre = st.text_input(
        "Nombre del negocio",
        placeholder="Ej. Casa Lenca"
    )

    st.subheader("Evaluación del negocio")

    # ======================================
    # MERCADO
    # ======================================

    st.subheader("🌎 Análisis del mercado")

    poblacion = st.number_input(
        "Población del área de mercado",
        min_value=0,
        value=25000,
        step=100
    )

    porcentaje_objetivo = st.number_input(
        "Porcentaje estimado del mercado objetivo (%)",
        min_value=0.0,
        max_value=100.0,
        value=35.0,
        step=1.0
    )

    frecuencia_compra = st.number_input(
        "Frecuencia promedio de compra mensual",
        min_value=0.0,
        value=2.5,
        step=0.1
    )

    ventas_estimadas = st.number_input(
        "Unidades vendidas estimadas mensualmente",
        min_value=0,
        value=15000,
        step=100
    )

    crecimiento = st.number_input(
        "Crecimiento estimado del mercado (%)",
        min_value=-100.0,
        value=6.0,
        step=0.5
    )

    accesibilidad = st.slider(
        "Accesibilidad al mercado",
        0,
        100,
        80
    )

    datos_mercado = {

        "poblacion": poblacion,
        "porcentaje_objetivo": porcentaje_objetivo,
        "frecuencia_compra": frecuencia_compra,
        "ventas_estimadas": ventas_estimadas,
        "crecimiento": crecimiento,
        "accesibilidad": accesibilidad
    }

    resultado_mercado = calcular_market_score(
        datos_mercado
    )

    # ======================================
    # RESULTADO MERCADO
    # ======================================

    st.divider()

    st.subheader(
        "📊 Resultado del análisis de mercado"
    )

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
    # PRODUCTO
    # ======================================

    st.divider()

    st.subheader("📦 Análisis del producto")

    necesidad = st.slider(
        "Necesidad que resuelve",
        0,
        100,
        50
    )

    valor_percibido = st.slider(
        "Valor percibido",
        0,
        100,
        50
    )

    diferenciacion = st.slider(
        "Diferenciación",
        0,
        100,
        50
    )

    calidad = st.slider(
        "Calidad esperada",
        0,
        100,
        50
    )

    innovacion = st.slider(
        "Innovación",
        0,
        100,
        50
    )

    sustitucion = st.slider(
        "Dificultad de sustitución",
        0,
        100,
        50
    )

    datos_producto = {

        "necesidad": necesidad,
        "valor_percibido": valor_percibido,
        "diferenciacion": diferenciacion,
        "calidad": calidad,
        "innovacion": innovacion,
        "sustitucion": sustitucion
    }

    resultado_producto = calcular_product_score(
        datos_producto
    )

    mostrar_resultado_engine(
    resultado_producto,
    "product_score",
    "📦 Análisis del producto"
    )


    # ======================================
    # RESTO DE INDICADORES
    # TEMPORALMENTE MANUALES
    # ======================================

    st.divider()

    st.subheader(
        "📋 Evaluación complementaria"
    )

# ======================================
# CLIENTE
# ======================================

st.divider()

st.subheader("👤 Análisis del cliente")

definicion_cliente = st.slider(
    "Claridad en la definición del cliente",
    0,
    100,
    50
)

necesidad_cliente = st.slider(
    "Necesidad del cliente",
    0,
    100,
    50
)

capacidad_pago = st.slider(
    "Capacidad de pago",
    0,
    100,
    50
)

accesibilidad_cliente = st.slider(
    "Accesibilidad al cliente",
    0,
    100,
    50
)

frecuencia_cliente = st.slider(
    "Frecuencia potencial de compra",
    0,
    100,
    50
)

tamano_segmento = st.slider(
    "Tamaño del segmento",
    0,
    100,
    50
)

datos_cliente = {

    "definicion_cliente": definicion_cliente,

    "necesidad": necesidad_cliente,

    "capacidad_pago": capacidad_pago,

    "accesibilidad": accesibilidad_cliente,

    "frecuencia": frecuencia_cliente,

    "tamano_segmento": tamano_segmento
}

resultado_cliente = calcular_customer_score(
    datos_cliente
)

mostrar_resultado_engine(
    resultado_cliente,
    "customer_score",
    "👤 Análisis del cliente"
)



# ======================================
# OTROS INDICADORES
# ======================================

# ======================================
# ACEPTACIÓN
# ======================================

st.divider()

st.subheader("❤️ Análisis de aceptación")

intencion = st.slider(
    "Intención de compra",
    0,
    100,
    50
)

relevancia = st.slider(
    "Relevancia del producto",
    0,
    100,
    50
)

disposicion_pago = st.slider(
    "Disposición a pagar",
    0,
    100,
    50
)

confianza = st.slider(
    "Confianza en el producto o marca",
    0,
    100,
    50
)

facilidad_compra = st.slider(
    "Facilidad de compra",
    0,
    100,
    50
)

barreras = st.slider(
    "Bajas barreras de compra",
    0,
    100,
    50
)

datos_aceptacion = {

    "intencion": intencion,

    "relevancia": relevancia,

    "disposicion_pago": disposicion_pago,

    "confianza": confianza,

    "facilidad_compra": facilidad_compra,

    "barreras": barreras
}

resultado_aceptacion = calcular_acceptance_score(
    datos_aceptacion
)

mostrar_resultado_engine(
    resultado_aceptacion,
    "acceptance_score",
    "❤️ Análisis de aceptación"
)

# ======================================
# COMPETENCIA
# ======================================

st.divider()

st.subheader("⚔️ Análisis de la competencia")

competencia_directa = st.slider(
    "Fortaleza frente a competidores directos",
    0,
    100,
    50
)

cantidad_competidores = st.slider(
    "Facilidad para competir frente a la cantidad de competidores",
    0,
    100,
    50
)

intensidad = st.slider(
    "Intensidad competitiva favorable",
    0,
    100,
    50
)

ventajas_competidores = st.slider(
    "Capacidad para enfrentar las ventajas de los competidores",
    0,
    100,
    50
)

barreras_entrada = st.slider(
    "Barreras de entrada del mercado",
    0,
    100,
    50
)

diferenciacion_competencia = st.slider(
    "Diferenciación frente a competidores",
    0,
    100,
    50
)

# ======================================
# DATOS DE COMPETENCIA
# ======================================

datos_competencia = {

    "competencia_directa":
        competencia_directa,

    "cantidad_competidores":
        cantidad_competidores,

    "intensidad":
        intensidad,

    "ventajas_competidores":
        ventajas_competidores,

    "barreras_entrada":
        barreras_entrada,

    "diferenciacion":
        diferenciacion_competencia
}

# ======================================
# CALCULAR COMPETITION SCORE
# ======================================

resultado_competencia = calcular_competition_score(
    datos_competencia
)

# ======================================
# MOSTRAR RESULTADO
# ======================================

mostrar_resultado_engine(
    resultado_competencia,
    "competition_score",
    "⚔️ Análisis de la competencia"
)

# ======================================
# POSICIONAMIENTO
# ======================================

st.divider()

st.subheader("🎯 Análisis del posicionamiento")

claridad_marca = st.slider(
    "Claridad de la marca",
    0,
    100,
    50
)

propuesta_valor = st.slider(
    "Claridad de la propuesta de valor",
    0,
    100,
    50
)

diferenciacion_posicionamiento = st.slider(
    "Diferenciación frente al mercado",
    0,
    100,
    50
)

posicionamiento_precio = st.slider(
    "Adecuación del posicionamiento de precio",
    0,
    100,
    50
)

reconocimiento = st.slider(
    "Reconocimiento de marca",
    0,
    100,
    50
)

coherencia = st.slider(
    "Coherencia entre marca, producto y mercado",
    0,
    100,
    50
)

datos_posicionamiento = {

    "claridad_marca":
        claridad_marca,

    "propuesta_valor":
        propuesta_valor,

    "diferenciacion":
        diferenciacion_posicionamiento,

    "posicionamiento_precio":
        posicionamiento_precio,

    "reconocimiento":
        reconocimiento,

    "coherencia":
        coherencia
}

resultado_posicionamiento = calcular_positioning_score(
    datos_posicionamiento
)

mostrar_resultado_engine(
    resultado_posicionamiento,
    "positioning_score",
    "🎯 Análisis del posicionamiento"
)

# ======================================
# FINANZAS
# ======================================

st.divider()

st.subheader("💰 Análisis financiero")

inversion_inicial = st.number_input(
    "Inversión inicial (L)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

precio_venta = st.number_input(
    "Precio promedio de venta por unidad (L)",
    min_value=0.0,
    value=0.0,
    step=1.0
)

unidades_mensuales = st.number_input(
    "Unidades vendidas mensualmente",
    min_value=0,
    value=0,
    step=100
)

costo_variable = st.number_input(
    "Costo variable por unidad (L)",
    min_value=0.0,
    value=0.0,
    step=0.50
)

costos_fijos = st.number_input(
    "Costos fijos mensuales (L)",
    min_value=0.0,
    value=0.0,
    step=1000.0
)


datos_finanzas = {

    "inversion_inicial":
        inversion_inicial,

    "precio_venta":
        precio_venta,

    "unidades_mensuales":
        unidades_mensuales,

    "costo_variable":
        costo_variable,

    "costos_fijos":
        costos_fijos
}

resultado_finanzas = calcular_finance_score(
    datos_finanzas
)

mostrar_resultado_engine(
    resultado_finanzas,
    "finance_score",
    "💰 Análisis financiero"
)

st.subheader("💵 Resumen financiero")

fin_col1, fin_col2, fin_col3 = st.columns(3)

with fin_col1:

    st.metric(
        "Ingresos mensuales",
        f"L {resultado_finanzas['ingresos_mensuales']:,.2f}"
    )

with fin_col2:

    st.metric(
        "Costos mensuales",
        f"L {resultado_finanzas['costo_total_mensual']:,.2f}"
    )

with fin_col3:

    st.metric(
        "Utilidad mensual",
        f"L {resultado_finanzas['utilidad_mensual']:,.2f}"
    )

fin_col1, fin_col2, fin_col3 = st.columns(3)

with fin_col1:

    st.metric(
        "Punto de equilibrio",
        f"{resultado_finanzas['punto_equilibrio_unidades']:,.0f} unidades"
    )

with fin_col2:

    st.metric(
        "ROI mensual",
        f"{resultado_finanzas['roi_mensual']:.2f}%"
    )

with fin_col3:

    st.metric(
        "Recuperación",
        (
            f"{resultado_finanzas['recuperacion_meses']:.1f} meses"
            if resultado_finanzas["recuperacion_meses"] > 0
            else "No recuperable"
        )
    )

# ======================================
# RIESGO
# ======================================

# ======================================
# MATRIZ VISUAL DE RIESGO
# ======================================

st.subheader("📊 Matriz de riesgos")

st.caption(
    "Nivel de riesgo = Probabilidad × Impacto"
)

# ======================================
# DATOS DE LA MATRIZ
# ======================================

probabilidades = [5, 4, 3, 2, 1]
impactos = [1, 2, 3, 4, 5]

z = []

for probabilidad in probabilidades:

    fila = []

    for impacto in impactos:

        nivel = probabilidad * impacto

        fila.append(nivel)

    z.append(fila)


# ======================================
# MATRIZ PLOTLY
# ======================================

figura_riesgo = go.Figure(
    data=go.Heatmap(

        z=z,

        x=impactos,

        y=probabilidades,

        text=z,

        texttemplate="%{text}",

        textfont={
            "size": 20
        },

        colorscale=[
            [0.00, "#27ae60"],
            [0.20, "#27ae60"],

            [0.21, "#f1c40f"],
            [0.40, "#f1c40f"],

            [0.41, "#e67e22"],
            [0.60, "#e67e22"],

            [0.61, "#e74c3c"],
            [1.00, "#e74c3c"]
        ],

        zmin=1,

        zmax=25,

        showscale=False,

        hovertemplate=
            "Probabilidad: %{y}<br>" +
            "Impacto: %{x}<br>" +
            "Nivel: %{z}<extra></extra>"
    )
)


# ======================================
# DISEÑO
# ======================================

figura_riesgo.update_layout(

    title={
        "text": "MATRIZ DE RIESGO",
        "x": 0.5,
        "xanchor": "center"
    },

    xaxis=dict(

        title="Impacto",

        tickmode="array",

        tickvals=impactos,

        ticktext=[
            "1 - Muy bajo",
            "2 - Bajo",
            "3 - Medio",
            "4 - Alto",
            "5 - Muy alto"
        ]
    ),

    yaxis=dict(

        title="Probabilidad",

        tickmode="array",

        tickvals=probabilidades,

        ticktext=[
            "5 - Muy alta",
            "4 - Alta",
            "3 - Media",
            "2 - Baja",
            "1 - Muy baja"
        ]
    ),

    height=600,

    margin=dict(
        l=80,
        r=30,
        t=80,
        b=80
    )
)


# ======================================
# MOSTRAR MATRIZ
# ======================================

st.plotly_chart(
    figura_riesgo,
    use_container_width=True
)


# ======================================
# LEYENDA
# ======================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.success(
        "🟢 BAJO\n\n1 – 5"
    )

with col2:

    st.warning(
        "🟡 MEDIO\n\n6 – 10"
    )

with col3:

    st.info(
        "🟠 ALTO\n\n11 – 15"
    )

with col4:

    st.error(
        "🔴 CRÍTICO\n\n16 – 25"
    )

# ======================================
# CERRAR CONTENEDOR
# ======================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# ======================================
# ANALIZAR
# ======================================

if st.button(
    "🚀 Analizar negocio",
    type="primary",
    use_container_width=True
):

    if not nombre:

        st.warning(
            "Debe ingresar el nombre del negocio."
        )

    else:

        scores = {

            "mercado":
                resultado_mercado["market_score"],

            "producto":
                resultado_producto["product_score"],

            "cliente":
                resultado_cliente["customer_score"],

            "aceptacion":
    		resultado_aceptacion["acceptance_score"],

            "competencia": 
                resultado_competencia["competition_score"],

            "posicionamiento":
                resultado_posicionamiento["positioning_score"],

            "finanzas":
                resultado_finanzas["finance_score"],

            "riesgo":
                resultado_riesgo["risk_score"],
        }

        resultado = analizar_negocio(
            nombre,
            scores
        )

        guardar_negocio(resultado)

        st.success(
            "Análisis completado y guardado correctamente."
        )

        # ==================================
        # RESULTADO PRINCIPAL
        # ==================================

        st.divider()

        st.subheader(
            "📊 Resultado del análisis"
        )

        resultado_col1, resultado_col2, resultado_col3 = st.columns(3)

        with resultado_col1:

            st.metric(
                "BUSINESS SCORE",
                f"{resultado['business_score']:.2f}/100"
            )

        with resultado_col2:

            st.metric(
                "Market Score",
                f"{scores['mercado']:.2f}/100"
            )

        with resultado_col3:

            st.metric(
                "Product Score",
                f"{scores['producto']:.2f}/100"
            )


        # ==================================
        # INDICADORES
        # ==================================

        st.divider()

        st.subheader(
            "📊 Indicadores"
        )

        nombres = {

            "mercado": "Mercado",
            "producto": "Producto",
            "cliente": "Cliente",
            "aceptacion": "Aceptación",
            "competencia": "Competencia",
            "posicionamiento": "Posicionamiento",
            "finanzas": "Finanzas",
            "riesgo": "Riesgo"
        }

        score_cols = st.columns(4)

        for i, categoria in enumerate(scores):

            with score_cols[i % 4]:

                st.metric(
                    nombres[categoria],
                    f"{scores[categoria]:.0f}/100"
                )

        # ==================================
        # RADAR
        # ==================================

        st.subheader(
            "🎯 Perfil del negocio"
        )

        categorias = list(scores.keys())

        valores = list(scores.values())

        categorias_radar = [
            nombres[x]
            for x in categorias
        ]

        valores_radar = valores + [
            valores[0]
        ]

        categorias_radar = (
            categorias_radar +
            [categorias_radar[0]]
        )

        figura = go.Figure()

        figura.add_trace(
            go.Scatterpolar(
                r=valores_radar,
                theta=categorias_radar,
                fill="toself",
                name=nombre
            )
        )

        figura.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True
        )

        st.plotly_chart(
            figura,
            use_container_width=True
        )

        # ==================================
        # DIAGNÓSTICO
        # ==================================

        st.subheader(
            "🧠 Diagnóstico"
        )

        st.write(
            resultado["diagnostico"]
        )

        # ==================================
        # ALERTAS
        # ==================================

        if resultado["alertas"]:

            st.subheader(
                "⚠️ Alertas"
            )

            for alerta in resultado["alertas"]:

                st.warning(
                    alerta
                )

        else:

            st.success(
                "No se detectaron alertas críticas."
            )
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