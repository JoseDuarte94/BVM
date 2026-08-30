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
from dashboard import mostrar_dashboard

from database import (
    inicializar_base_datos,
    guardar_negocio,
    obtener_negocios,
    obtener_riesgos_por_negocio,
    eliminar_negocio,
    guardar_analisis_ia,
    obtener_analisis_ia
)

from ai_engine import generar_analisis_ia

from chat_engine import enviar_mensaje_chat


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Business Validation Model",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# PROTECCIÓN CON CONTRASEÑA
#
# Solo se activa si configuras APP_PASSWORD en
# los secrets (st.secrets). Si no la configuras
# (por ejemplo, corriendo en tu máquina local),
# la app funciona normal, sin pedir nada.
# ==========================================

def _hay_password_configurada():

    try:
        return bool(st.secrets.get("APP_PASSWORD"))
    except Exception:
        return False


def _verificar_acceso():

    if not _hay_password_configurada():
        return True

    if st.session_state.get("acceso_concedido", False):
        return True

    st.title("📊 Business Validation Model")

    st.caption("Esta aplicación es privada.")

    def _revisar_password():

        if st.session_state.get("password_ingresada") == st.secrets["APP_PASSWORD"]:
            st.session_state["acceso_concedido"] = True
        else:
            st.session_state["acceso_concedido"] = False

    st.text_input(
        "Contraseña",
        type="password",
        key="password_ingresada",
        on_change=_revisar_password
    )

    if st.session_state.get("acceso_concedido") is False:
        st.error("Contraseña incorrecta.")

    return False


if not _verificar_acceso():
    st.stop()


inicializar_base_datos()


# ==========================================
# API KEY DE IA (ANTHROPIC O GEMINI)
#
# Cada proveedor busca su key en este orden:
# 1. st.secrets["..._API_KEY"] (recomendado
#    para producción — archivo .streamlit/secrets.toml)
# 2. Variable de entorno "..._API_KEY"
# 3. Campo manual en la barra lateral (solo dura
#    la sesión del navegador, nunca se guarda en
#    la base de datos ni en disco)
# ==========================================

import os

NOMBRE_VARIABLE_KEY = {
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY"
}

def obtener_proveedor_ia():

    return st.session_state.get("proveedor_ia", "gemini")


def obtener_api_key(proveedor=None):

    proveedor = proveedor or obtener_proveedor_ia()

    nombre_variable = NOMBRE_VARIABLE_KEY[proveedor]

    try:
        if nombre_variable in st.secrets:
            return st.secrets[nombre_variable]
    except Exception:
        pass

    if os.environ.get(nombre_variable):
        return os.environ[nombre_variable]

    return st.session_state.get(f"api_key_manual_{proveedor}", "")


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
        "🤖 Asistente IA",
        "Dashboard",
        "Proyectos guardados"
    ]
)

with st.sidebar.expander("🔑 Conexión con IA", expanded=True):

    st.session_state["proveedor_ia"] = st.radio(
        "Proveedor",
        ["gemini", "anthropic"],
        format_func=lambda x: (
            "Google Gemini (gratis)"
            if x == "gemini"
            else "Anthropic Claude (de pago)"
        ),
        horizontal=True,
        key="selector_proveedor_ia"
    )

    proveedor_actual = st.session_state["proveedor_ia"]

    api_key_detectada = obtener_api_key(proveedor_actual)

    if api_key_detectada:

        st.success("API key configurada correctamente.")

    else:

        etiqueta_proveedor = (
            "Gemini" if proveedor_actual == "gemini" else "Anthropic"
        )

        st.caption(
            f"No se detectó una API key de {etiqueta_proveedor} en "
            "secrets.toml ni en variables de entorno. Pégala aquí "
            "para esta sesión:"
        )

        if proveedor_actual == "gemini":

            st.caption(
                "Consíguela gratis en https://aistudio.google.com/apikey"
            )

        clave_sesion = f"api_key_manual_{proveedor_actual}"

        st.session_state[clave_sesion] = st.text_input(
            f"API key de {etiqueta_proveedor}",
            type="password",
            value=st.session_state.get(clave_sesion, ""),
            key=f"input_{clave_sesion}"
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

def clasificar_business_score(score):

    if score >= 85:
        return "EXCELENTE", "🟢"

    elif score >= 70:
        return "FAVORABLE", "🟢"

    elif score >= 55:
        return "MODERADO", "🟡"

    elif score >= 40:
        return "DÉBIL", "🟠"

    else:
        return "CRÍTICO", "🔴"


# ==========================================
# CORRER LOS 8 ENGINES A PARTIR DE LOS DATOS
# ESTRUCTURADOS QUE DEVUELVE EL ASISTENTE IA
# ==========================================

def ejecutar_analisis_desde_datos_ia(datos):
    """
    Toma el diccionario que devolvió la IA en el chat (con las
    claves nombre, mercado, producto, cliente, aceptacion,
    competencia, posicionamiento, finanzas, riesgos) y corre los
    mismos 8 engines + risk engine que usa "Nuevo análisis", pero
    a partir de datos generados por la IA en vez de sliders.

    Devuelve (resultado, resultado_riesgo). Lanza KeyError si a
    los datos les falta alguna sección — quien llame a esta
    función debe mostrarlo como un error legible.
    """

    resultado_mercado = calcular_market_score(datos["mercado"])
    resultado_producto = calcular_product_score(datos["producto"])
    resultado_cliente = calcular_customer_score(datos["cliente"])
    resultado_aceptacion = calcular_acceptance_score(datos["aceptacion"])
    resultado_competencia = calcular_competition_score(datos["competencia"])
    resultado_posicionamiento = calcular_positioning_score(
        datos["posicionamiento"]
    )
    resultado_finanzas = calcular_finance_score(datos["finanzas"])

    riesgos_lista = datos.get("riesgos", [])

    resultado_riesgo = calcular_risk_score(riesgos_lista)

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

    resultado = analizar_negocio(
        datos.get("nombre", "Negocio sin nombre"),
        scores
    )

    return resultado, resultado_riesgo


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

    st.divider()

    st.subheader("⚠️ Evaluación de riesgos")

    st.caption(
        "Registre los riesgos del proyecto y evalúe su probabilidad "
        "e impacto en una escala de 1 a 5."
    )

    # ======================================
    # LISTA DE RIESGOS
    # ======================================

    if "lista_riesgos" not in st.session_state:

        st.session_state.lista_riesgos = []


    # ======================================
    # FORMULARIO PARA AGREGAR RIESGO
    # ======================================

    riesgo_col1, riesgo_col2 = st.columns(2)

    with riesgo_col1:

        nombre_riesgo = st.text_input(
            "Nombre del riesgo",
            placeholder="Ej. Demanda insuficiente"
        )

    with riesgo_col2:

        area_riesgo = st.selectbox(
            "Área asociada",
            [
                "Mercado",
                "Producto",
                "Cliente",
                "Competencia",
                "Posicionamiento",
                "Finanzas",
                "Operación",
                "Legal",
                "Otro"
            ]
        )


    riesgo_col3, riesgo_col4 = st.columns(2)

    with riesgo_col3:

        probabilidad_riesgo = st.slider(
            "Probabilidad de ocurrencia",
            1,
            5,
            3,
            format="%d / 5"
        )

    with riesgo_col4:

        impacto_riesgo = st.slider(
            "Impacto si ocurre",
            1,
            5,
            3,
            format="%d / 5"
        )


    # ======================================
    # CALCULAR NIVEL DEL RIESGO ACTUAL
    # ======================================

    nivel_actual = (
        probabilidad_riesgo *
        impacto_riesgo
    )


    if nivel_actual <= 5:

        categoria_actual = "BAJO"
        emoji_actual = "🟢"

    elif nivel_actual <= 10:

        categoria_actual = "MEDIO"
        emoji_actual = "🟡"

    elif nivel_actual <= 20:

        categoria_actual = "ALTO"
        emoji_actual = "🟠"

    else:

        categoria_actual = "CRÍTICO"
        emoji_actual = "🔴"


    # ======================================
    # VISTA PREVIA DEL RIESGO
    # ======================================

    # ======================================
    # AGREGAR RIESGO
    # ======================================

    if st.button(
        "➕ Agregar riesgo",
        use_container_width=True
    ):

        if not nombre_riesgo.strip():

            st.warning(
                "Debe ingresar el nombre del riesgo."
            )

        else:

            st.session_state.lista_riesgos.append({

                "riesgo": nombre_riesgo,

                "area": area_riesgo,

                "probabilidad":
                    probabilidad_riesgo,

                "impacto":
                    impacto_riesgo
            })

            st.success(
                f"Riesgo '{nombre_riesgo}' agregado correctamente."
            )

            st.rerun()


    # ======================================
    # RIESGOS REGISTRADOS
    # ======================================

    st.divider()

    st.subheader("📋 Riesgos registrados")


    if st.session_state.lista_riesgos:

        # ----------------------------------
        # ENCABEZADOS
        # ----------------------------------

        encabezado = st.columns(
            [3, 2, 1.2, 1.2, 1.3, 2.5]
        )

        with encabezado[0]:

            st.write("**Riesgo**")

        with encabezado[1]:

            st.write("**Área**")

        with encabezado[2]:

            st.write("**Prob.**")

        with encabezado[3]:

            st.write("**Impacto**")

        with encabezado[4]:

            st.write("**Nivel**")

        with encabezado[5]:

            st.write("**Clasificación**")


        # ----------------------------------
        # FILAS
        # ----------------------------------

        for indice, riesgo_item in enumerate(
            st.session_state.lista_riesgos
        ):

            probabilidad = riesgo_item["probabilidad"]

            impacto = riesgo_item["impacto"]

            nivel = probabilidad * impacto


            if nivel <= 5:

                color = "#27ae60"
                clasificacion = "BAJO"

            elif nivel <= 10:

                color = "#f1c40f"
                clasificacion = "MEDIO"

            elif nivel <= 20:

                color = "#e67e22"
                clasificacion = "ALTO"

            else:

                color = "#e74c3c"
                clasificacion = "CRÍTICO"


            fila = st.columns(
                [3, 2, 1.2, 1.2, 1.3, 2.5]
            )


            with fila[0]:

                st.write(
                    f"**{riesgo_item['riesgo']}**"
                )


            with fila[1]:

                st.write(
                    riesgo_item["area"]
                )


            with fila[2]:

                st.write(
                    str(probabilidad)
                )


            with fila[3]:

                st.write(
                    str(impacto)
                )


            # ----------------------------------
            # CELDA DE NIVEL CON COLOR
            # ----------------------------------

            with fila[4]:

                st.markdown(
                    f"""
                    <div style="
                        background:{color};
                        color:white;
                        border-radius:8px;
                        padding:8px;
                        text-align:center;
                        font-weight:bold;
                    ">
                        {nivel}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with fila[5]:

                st.write(
                    clasificacion
                )


            # ----------------------------------
            # ELIMINAR
            # ----------------------------------

            if st.button(
                "🗑️ Eliminar",
                key=f"eliminar_riesgo_{indice}"
            ):

                st.session_state.lista_riesgos.pop(indice)

                st.rerun()


            st.divider()


        # ==================================
        # VACIAR RIESGOS
        # ==================================

        if st.button(
            "🗑️ Vaciar todos los riesgos"
        ):

            st.session_state.lista_riesgos = []

            st.rerun()


    else:

        st.info(
            "Todavía no hay riesgos registrados. "
            "Agregue al menos un riesgo para generar el análisis."
        )


    # ======================================
    # RISK ENGINE (SIEMPRE SE CALCULA, HAYA
    # O NO RIESGOS REGISTRADOS)
    # ======================================

    resultado_riesgo = calcular_risk_score(
        st.session_state.lista_riesgos
    )

    # ======================================
    # MATRIZ DE DISTRIBUCIÓN
    # ======================================

    if st.session_state.lista_riesgos:

        st.divider()

        st.subheader("📊 Resumen de la matriz de riesgo")


        # ----------------------------------
        # CALCULAR NIVELES
        # ----------------------------------

        niveles = [

            riesgo["probabilidad"] *
            riesgo["impacto"]

            for riesgo
            in st.session_state.lista_riesgos
        ]


        bajos = sum(
            1
            for nivel in niveles
            if nivel <= 5
        )


        medios = sum(
            1
            for nivel in niveles
            if 6 <= nivel <= 10
        )


        altos = sum(
            1
            for nivel in niveles
            if 11 <= nivel <= 20
        )


        criticos = sum(
            1
            for nivel in niveles
            if nivel >= 21
        )


        promedio = (
            sum(niveles) /
            len(niveles)
        )


        maximo = max(niveles)


        # ==================================
        # INDICADORES
        # ==================================

        resumen1, resumen2, resumen3, resumen4 = st.columns(4)


        with resumen1:

            st.metric(
                "🟢 Riesgos bajos",
                bajos
            )


        with resumen2:

            st.metric(
                "🟡 Riesgos medios",
                medios
            )


        with resumen3:

            st.metric(
                "🟠 Riesgos altos",
                altos
            )


        with resumen4:

            st.metric(
                "🔴 Riesgos críticos",
                criticos
            )


        st.divider()


        resumen5, resumen6, resumen7 = st.columns(3)


        with resumen5:

            st.metric(
                "Promedio de riesgo",
                f"{promedio:.2f} / 25"
            )


        with resumen6:

            st.metric(
                "Nivel máximo",
                f"{maximo} / 25"
            )


        with resumen7:

            st.metric(
                "RISK SCORE",
                f"{resultado_riesgo['risk_score']:.2f}/100"
            )


        # ==================================
        # DIAGNÓSTICO
        # ==================================

        st.subheader("🧠 Diagnóstico de riesgo")


        if criticos > 0:

            st.error(
                f"🔴 Se identificaron **{criticos} riesgo(s) crítico(s)**. "
                "Se recomienda atenderlos antes de tomar una decisión "
                "de inversión."
            )

        elif altos > 0:

            st.warning(
                f"🟠 Se identificaron **{altos} riesgo(s) alto(s)**. "
                "El proyecto requiere medidas de mitigación."
            )

        elif medios > 0:

            st.info(
                f"🟡 Se identificaron **{medios} riesgo(s) medio(s)**. "
                "Se recomienda establecer controles y monitoreo."
            )

        else:

            st.success(
                "🟢 Los riesgos registrados se encuentran en "
                "niveles bajos."
            )


        # ==================================
        # RESULTADO COMPLETO DEL ENGINE
        # ==================================

        mostrar_resultado_engine(
            resultado_riesgo,
            "risk_score",
            "🚨 Análisis de riesgo"
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

            negocio_id_guardado = guardar_negocio(
                resultado,
                resultado_riesgo["riesgos"]
            )

            st.success(
                "Análisis guardado correctamente."
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

            # ==================================
            # ANÁLISIS CUALITATIVO CON IA
            # ==================================

            st.divider()

            st.subheader(
                "🤖 Análisis cualitativo con IA"
            )

            st.caption(
                "Complementa el diagnóstico automático con un análisis "
                "ejecutivo generado por IA a partir de estos mismos resultados."
            )

            if st.button(
                "🤖 Generar análisis con IA",
                key=f"generar_ia_{negocio_id_guardado}"
            ):

                proveedor_ia_actual = obtener_proveedor_ia()

                api_key_actual = obtener_api_key(proveedor_ia_actual)

                if not api_key_actual:

                    st.error(
                        "No hay una API key configurada para el proveedor "
                        "seleccionado. Ábrela en '🔑 Conexión con IA' en "
                        "la barra lateral."
                    )

                else:

                    with st.spinner("Generando análisis con IA..."):

                        try:

                            texto_ia = generar_analisis_ia(
                                resultado,
                                resultado_riesgo["riesgos"],
                                api_key_actual,
                                proveedor_ia_actual
                            )

                            guardar_analisis_ia(
                                negocio_id_guardado,
                                texto_ia
                            )

                            st.markdown(texto_ia)

                        except Exception as error:

                            st.error(
                                f"No se pudo generar el análisis con IA: {error}"
                            )

# ==========================================
# ASISTENTE IA (CHAT)
# ==========================================

elif opcion == "🤖 Asistente IA":

    st.header("🤖 Asistente de análisis con IA")

    st.caption(
        "Descríbele tu idea de negocio y dale los datos financieros y de "
        "mercado que te pida. La IA estimará el resto de los indicadores "
        "cualitativos y armará el análisis completo — tú revisas los "
        "valores antes de guardarlo."
    )

    if "chat_historial" not in st.session_state:
        st.session_state.chat_historial = []

    if "chat_datos_listos" not in st.session_state:
        st.session_state.chat_datos_listos = None

    # ======================================
    # MOSTRAR HISTORIAL
    # ======================================

    for mensaje in st.session_state.chat_historial:

        with st.chat_message(mensaje["role"]):

            st.markdown(mensaje["content"])

            fuentes_mensaje = mensaje.get("fuentes")

            if fuentes_mensaje:

                with st.expander(
                    f"🔍 {len(fuentes_mensaje)} fuente(s) consultada(s)"
                ):

                    for fuente in fuentes_mensaje:

                        titulo_fuente = fuente.get("titulo") or fuente.get("url")

                        url_fuente = fuente.get("url")

                        if url_fuente:
                            st.markdown(f"- [{titulo_fuente}]({url_fuente})")
                        else:
                            st.markdown(f"- {titulo_fuente}")

    # ======================================
    # ENTRADA DEL USUARIO
    # ======================================

    entrada_chat = st.chat_input(
        "Describe tu negocio, o responde lo que te pida la IA..."
    )

    if entrada_chat:

        st.session_state.chat_historial.append({
            "role": "user",
            "content": entrada_chat
        })

        with st.chat_message("user"):

            st.markdown(entrada_chat)

        proveedor_chat = obtener_proveedor_ia()

        api_key_chat = obtener_api_key(proveedor_chat)

        with st.chat_message("assistant"):

            if not api_key_chat:

                st.error(
                    "No hay una API key configurada para el proveedor "
                    "seleccionado. Ábrela en '🔑 Conexión con IA' en "
                    "la barra lateral."
                )

            else:

                with st.spinner("Investigando y pensando..."):

                    try:

                        texto_respuesta, datos_extraidos, fuentes_respuesta = (
                            enviar_mensaje_chat(
                                st.session_state.chat_historial,
                                api_key_chat,
                                proveedor_chat
                            )
                        )

                        st.markdown(texto_respuesta)

                        if fuentes_respuesta:

                            with st.expander(
                                f"🔍 {len(fuentes_respuesta)} fuente(s) consultada(s)"
                            ):

                                for fuente in fuentes_respuesta:

                                    titulo_fuente = (
                                        fuente.get("titulo") or fuente.get("url")
                                    )

                                    url_fuente = fuente.get("url")

                                    if url_fuente:
                                        st.markdown(
                                            f"- [{titulo_fuente}]({url_fuente})"
                                        )
                                    else:
                                        st.markdown(f"- {titulo_fuente}")

                        st.session_state.chat_historial.append({
                            "role": "assistant",
                            "content": texto_respuesta,
                            "fuentes": fuentes_respuesta
                        })

                        if datos_extraidos:

                            st.session_state.chat_datos_listos = datos_extraidos

                    except Exception as error:

                        st.error(
                            f"No se pudo obtener respuesta de la IA: {error}"
                        )

    # ======================================
    # DATOS LISTOS: VISTA PREVIA Y EJECUCIÓN
    # ======================================

    if st.session_state.chat_datos_listos:

        st.divider()

        st.success(
            "La IA reunió toda la información necesaria. Revisa los "
            "valores antes de generar el análisis:"
        )

        datos_ia = st.session_state.chat_datos_listos

        with st.expander("📋 Ver datos que la IA va a usar", expanded=True):

            st.write(f"**Nombre del negocio:** {datos_ia.get('nombre', '—')}")

            columnas_datos = st.columns(2)

            categorias_datos = [
                ("mercado", "🌎 Mercado"),
                ("producto", "📦 Producto"),
                ("cliente", "👤 Cliente"),
                ("aceptacion", "❤️ Aceptación"),
                ("competencia", "⚔️ Competencia"),
                ("posicionamiento", "🎯 Posicionamiento")
            ]

            for indice, (clave, titulo) in enumerate(categorias_datos):

                with columnas_datos[indice % 2]:

                    st.write(f"**{titulo}**")

                    st.json(datos_ia.get(clave, {}))

            st.write("**💰 Finanzas**")

            st.json(datos_ia.get("finanzas", {}))

            st.write("**🚨 Riesgos identificados**")

            riesgos_ia = datos_ia.get("riesgos", [])

            if riesgos_ia:

                for riesgo_item in riesgos_ia:

                    st.write(
                        f"- **{riesgo_item.get('riesgo', '—')}** "
                        f"({riesgo_item.get('area', '—')}) — "
                        f"P: {riesgo_item.get('probabilidad', '—')}, "
                        f"I: {riesgo_item.get('impacto', '—')}"
                    )

            else:

                st.caption("La IA no identificó riesgos.")

        boton_col1, boton_col2 = st.columns(2)

        with boton_col1:

            if st.button(
                "🚀 Ejecutar análisis con estos datos",
                type="primary",
                use_container_width=True
            ):

                try:

                    resultado_ia, resultado_riesgo_ia = (
                        ejecutar_analisis_desde_datos_ia(datos_ia)
                    )

                    negocio_id_ia = guardar_negocio(
                        resultado_ia,
                        resultado_riesgo_ia["riesgos"]
                    )

                    st.success(
                        "Análisis generado y guardado correctamente."
                    )

                    st.subheader("📊 Resultado del análisis")

                    resultado_col1, resultado_col2 = st.columns(2)

                    with resultado_col1:

                        st.metric(
                            "BUSINESS SCORE",
                            f"{resultado_ia['business_score']:.2f}/100"
                        )

                    with resultado_col2:

                        st.metric(
                            "Nivel de riesgo general",
                            resultado_ia["nivel_riesgo"]
                        )

                    st.write(
                        f"**Recomendación:** {resultado_ia['recomendacion']}"
                    )

                    st.write("#### 🧠 Diagnóstico")

                    st.write(resultado_ia["diagnostico"])

                    if resultado_ia["alertas"]:

                        st.write("#### ⚠️ Alertas")

                        for alerta in resultado_ia["alertas"]:

                            st.warning(alerta)

                    else:

                        st.success(
                            "No se detectaron alertas críticas."
                        )

                    st.info(
                        "Puedes ver este proyecto completo, incluido el "
                        "desglose por categoría, en '📁 Proyectos guardados'."
                    )

                    st.session_state.chat_datos_listos = None

                except KeyError as error:

                    st.error(
                        f"Los datos de la IA no tienen la sección "
                        f"esperada: {error}. Pídele a la IA que "
                        "complete la información faltante."
                    )

                    with st.expander("Ver detalle técnico del error"):

                        st.exception(error)

                except Exception as error:

                    st.error(
                        f"No se pudo generar el análisis: {error}"
                    )

                    with st.expander("Ver detalle técnico del error"):

                        st.exception(error)

        with boton_col2:

            if st.button(
                "🔄 Descartar y seguir conversando",
                use_container_width=True
            ):

                st.session_state.chat_datos_listos = None

                st.rerun()

    if st.session_state.chat_historial:

        st.divider()

        if st.button("🗑️ Reiniciar conversación"):

            st.session_state.chat_historial = []

            st.session_state.chat_datos_listos = None

            st.rerun()

# ==========================================
# DASHBOARD
# ==========================================

elif opcion == "Dashboard":

     mostrar_dashboard()

# ==========================================
# PROYECTOS GUARDADOS
# ==========================================

elif opcion == "Proyectos guardados":

    st.header("📁 Proyectos guardados")

    negocios = obtener_negocios()

    # ======================================
    # SIN PROYECTOS
    # ======================================

    if not negocios:

        st.info(
            "No existen proyectos guardados."
        )

    else:

        st.caption(
            f"Se encontraron {len(negocios)} proyectos analizados."
        )

        # ==================================
        # LISTA DE PROYECTOS
        # ==================================

        for negocio in negocios:

            id_negocio = negocio[0]
            nombre = negocio[1]
            score = negocio[10]
            recomendacion = negocio[11]
            nivel_riesgo = negocio[12]

            # ==================================
            # EXPANDER DEL PROYECTO
            # ==================================

            with st.expander(
                f"📊 {nombre} — Business Score: {score:.2f}/100"
            ):

                # ==================================
                # INFORMACIÓN PRINCIPAL
                # ==================================

                st.subheader(
                    f"📋 Análisis de {nombre}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Business Score",
                        f"{score:.2f}/100"
                    )

                with col2:

                    st.write(
                        "**Recomendación**"
                    )

                    st.info(
                        recomendacion
                    )

                with col3:

                    st.write(
                        "**Nivel de riesgo**"
                    )

                    if str(nivel_riesgo).upper() == "CRÍTICO":

                        st.error(
                            f"🔴 {nivel_riesgo}"
                        )

                    elif str(nivel_riesgo).upper() == "ALTO":

                        st.warning(
                            f"🟠 {nivel_riesgo}"
                        )

                    elif str(nivel_riesgo).upper() == "MEDIO":

                        st.warning(
                            f"🟡 {nivel_riesgo}"
                        )

                    else:

                        st.success(
                            f"🟢 {nivel_riesgo}"
                        )

                st.divider()

                # ==================================
                # SCORES DEL NEGOCIO
                # ==================================

                st.subheader(
                    "📊 Indicadores del negocio"
                )

                mercado = negocio[2]
                producto = negocio[3]
                cliente = negocio[4]
                aceptacion = negocio[5]
                competencia = negocio[6]
                posicionamiento = negocio[7]
                finanzas = negocio[8]
                riesgo = negocio[9]

                diagnostico = negocio[13]

                score_cols = st.columns(4)

                with score_cols[0]:

                    st.metric(
                        "🌎 Mercado",
                        f"{mercado:.0f}/100"
                    )

                with score_cols[1]:

                    st.metric(
                        "📦 Producto",
                        f"{producto:.0f}/100"
                    )

                with score_cols[2]:

                    st.metric(
                        "👤 Cliente",
                        f"{cliente:.0f}/100"
                    )

                with score_cols[3]:

                    st.metric(
                        "❤️ Aceptación",
                        f"{aceptacion:.0f}/100"
                    )

                score_cols = st.columns(4)

                with score_cols[0]:

                    st.metric(
                        "⚔️ Competencia",
                        f"{competencia:.0f}/100"
                    )

                with score_cols[1]:

                    st.metric(
                        "🎯 Posicionamiento",
                        f"{posicionamiento:.0f}/100"
                    )

                with score_cols[2]:

                    st.metric(
                        "💰 Finanzas",
                        f"{finanzas:.0f}/100"
                    )

                with score_cols[3]:

                    st.metric(
                        "⚠️ Riesgo",
                        f"{riesgo:.0f}/100"
                    )

                st.divider()

                # ==================================
                # DIAGNÓSTICO
                # ==================================

                st.subheader(
                    "🧠 Diagnóstico"
                )

                st.info(
                    diagnostico
                )

                # ==================================
                # RIESGOS DEL PROYECTO
                # ==================================

                st.divider()

                st.subheader(
                    "⚠️ Riesgos registrados"
                )

                riesgos_guardados = obtener_riesgos_por_negocio(
                    id_negocio
                )

                if riesgos_guardados:

                    for riesgo_item in riesgos_guardados:

                        (
                            riesgo_nombre,
                            area,
                            probabilidad,
                            impacto,
                            nivel,
                            clasificacion,
                            accion
                        ) = riesgo_item

                        riesgo_col1, riesgo_col2, riesgo_col3 = st.columns(
                            [3, 2, 2]
                        )

                        with riesgo_col1:

                            st.write(
                                f"**{riesgo_nombre}**"
                            )

                            st.caption(
                                f"Área: {area}"
                            )

                        with riesgo_col2:

                            st.write(
                                f"Probabilidad: {probabilidad}/5"
                            )

                            st.write(
                                f"Impacto: {impacto}/5"
                            )

                        with riesgo_col3:

                            if str(clasificacion).upper() == "CRÍTICO":

                                st.error(
                                    f"🔴 {clasificacion}"
                                )

                            elif str(clasificacion).upper() == "ALTO":

                                st.warning(
                                    f"🟠 {clasificacion}"
                                )

                            elif str(clasificacion).upper() == "MEDIO":

                                st.warning(
                                    f"🟡 {clasificacion}"
                                )

                            else:

                                st.success(
                                    f"🟢 {clasificacion}"
                                )

                            st.write(
                                f"Nivel: {nivel}/25"
                            )

                        st.caption(
                            f"Acción recomendada: {accion}"
                        )

                        st.divider()

                else:

                    st.info(
                        "Este proyecto no tiene riesgos "
                        "individuales registrados."
                    )

                # ==================================
                # ANÁLISIS CUALITATIVO CON IA
                # ==================================

                st.divider()

                st.subheader(
                    "🤖 Análisis cualitativo con IA"
                )

                analisis_ia_guardado = obtener_analisis_ia(
                    id_negocio
                )

                if analisis_ia_guardado:

                    st.markdown(analisis_ia_guardado)

                else:

                    st.caption(
                        "Este proyecto todavía no tiene un análisis "
                        "generado por IA."
                    )

                if st.button(
                    "🤖 " + (
                        "Regenerar análisis con IA"
                        if analisis_ia_guardado
                        else "Generar análisis con IA"
                    ),
                    key=f"generar_ia_guardado_{id_negocio}"
                ):

                    proveedor_ia_actual = obtener_proveedor_ia()

                    api_key_actual = obtener_api_key(proveedor_ia_actual)

                    if not api_key_actual:

                        st.error(
                            "No hay una API key configurada para el "
                            "proveedor seleccionado. Ábrela en "
                            "'🔑 Conexión con IA' en la barra lateral."
                        )

                    else:

                        with st.spinner("Generando análisis con IA..."):

                            try:

                                resultado_para_ia = {
                                    "nombre": nombre,
                                    "scores": {
                                        "mercado": mercado,
                                        "producto": producto,
                                        "cliente": cliente,
                                        "aceptacion": aceptacion,
                                        "competencia": competencia,
                                        "posicionamiento": posicionamiento,
                                        "finanzas": finanzas,
                                        "riesgo": riesgo
                                    },
                                    "business_score": score,
                                    "recomendacion": recomendacion,
                                    "nivel_riesgo": nivel_riesgo,
                                    "diagnostico": diagnostico,
                                    "alertas": []
                                }

                                riesgos_para_ia = [
                                    {
                                        "riesgo": r[0],
                                        "area": r[1],
                                        "probabilidad": r[2],
                                        "impacto": r[3],
                                        "nivel": r[4],
                                        "clasificacion": r[5]
                                    }
                                    for r in riesgos_guardados
                                ]

                                texto_ia = generar_analisis_ia(
                                    resultado_para_ia,
                                    riesgos_para_ia,
                                    api_key_actual,
                                    proveedor_ia_actual
                                )

                                guardar_analisis_ia(
                                    id_negocio,
                                    texto_ia
                                )

                                st.rerun()

                            except Exception as error:

                                st.error(
                                    f"No se pudo generar el análisis con IA: {error}"
                                )

                # ==================================
                # ELIMINAR PROYECTO
                # ==================================

                st.divider()

                st.subheader(
                    "🗑️ Gestión del proyecto"
                )

                confirmar = st.checkbox(
                    "Confirmar eliminación de este proyecto",
                    key=f"confirmar_eliminar_{id_negocio}"
                )

                if st.button(
                    "🗑️ Eliminar proyecto",
                    key=f"eliminar_proyecto_{id_negocio}",
                    type="secondary"
                ):

                    if confirmar:

                        eliminar_negocio(
                            id_negocio
                        )

                        st.success(
                            f"El proyecto '{nombre}' fue eliminado correctamente."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Debe confirmar la eliminación antes de continuar."
                        )

        # ==================================
        # SEPARACIÓN
        # ==================================

        st.divider()

        st.caption(
            "Los proyectos se muestran ordenados por Business Score."
        )