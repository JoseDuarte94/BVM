# ==========================================
# BVM AI ENGINE
#
# Genera un análisis ejecutivo cualitativo a
# partir de los resultados ya calculados por
# los 8 engines basados en reglas (mercado,
# producto, cliente, aceptación, competencia,
# posicionamiento, finanzas, riesgo).
#
# Este módulo NO reemplaza esos engines, los
# complementa: la IA recibe los números y
# diagnósticos que ya calculó cada uno y
# construye un análisis más humano, que cruza
# categorías y da recomendaciones concretas.
#
# Soporta dos proveedores intercambiables:
# - "anthropic" (Claude) — de pago, sin nivel
#   gratuito permanente en la API.
# - "gemini" (Google) — tiene un nivel gratuito
#   real (modelos Flash), sin tarjeta de crédito.
# ==========================================


# Cambia esto si tu cuenta usa otro modelo.
MODELO_ANTHROPIC = "claude-sonnet-5"

# gemini-3.6-flash es el modelo Flash vigente
# de Google con acceso gratuito en la API
# (gemini-2.5-flash fue retirado para cuentas
# nuevas). Si en el futuro Google lanza una
# versión más nueva, solo cambia esta línea.
MODELO_GEMINI = "gemini-3.6-flash"


import time


def _es_error_temporal(error):
    """
    Detecta errores de sobrecarga/disponibilidad temporal de los
    proveedores (503, 'overloaded', 'UNAVAILABLE', 429 de límite
    por minuto) para reintentar automáticamente. Errores de API
    key inválida, etc. NO se reintentan.
    """

    texto_error = str(error).upper()

    palabras_temporales = [
        "503",
        "UNAVAILABLE",
        "OVERLOADED",
        "HIGH DEMAND",
        "TIMEOUT",
        "529",
        "429",
        "RESOURCE_EXHAUSTED",
        "RATE LIMIT",
        "QUOTA"
    ]

    return any(palabra in texto_error for palabra in palabras_temporales)


def _con_reintentos(funcion, intentos=4, espera_inicial=5):
    """
    Ejecuta 'funcion' (sin argumentos) reintentando con espera
    progresiva (5s, 10s, 20s...) solo si el error parece temporal.
    Si se agotan los intentos, o el error no es temporal, se
    relanza la excepción original tal cual.
    """

    espera = espera_inicial

    for intento in range(1, intentos + 1):

        try:
            return funcion()

        except Exception as error:

            es_ultimo_intento = intento == intentos

            if es_ultimo_intento or not _es_error_temporal(error):
                raise

            time.sleep(espera)

            espera *= 2


def _construir_prompt(resultado, riesgos_detalle=None):

    scores = resultado["scores"]

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

    lineas_scores = "\n".join(
        f"- {nombres_categorias[categoria]}: {valor:.1f}/100"
        for categoria, valor in scores.items()
    )

    lineas_riesgos = "Sin riesgos individuales registrados."

    if riesgos_detalle:

        lineas_riesgos = "\n".join(
            f"- {r['riesgo']} (área: {r['area']}) — "
            f"probabilidad {r['probabilidad']}/5, "
            f"impacto {r['impacto']}/5, "
            f"nivel {r['nivel']}/25, "
            f"clasificación {r['clasificacion']}"
            for r in riesgos_detalle
        )

    alertas = resultado.get("alertas") or []

    lineas_alertas = (
        "\n".join(f"- {a}" for a in alertas)
        if alertas
        else "Sin alertas registradas."
    )

    prompt = f"""Eres un consultor experto en validación de modelos de negocio.

A continuación tienes los resultados de un análisis cuantitativo (basado en reglas) \
de un negocio llamado "{resultado['nombre']}". Tu trabajo es leer estos números y \
generar un análisis ejecutivo cualitativo en español, NO recalcular los scores.

BUSINESS SCORE GENERAL: {resultado['business_score']:.1f}/100
RECOMENDACIÓN DEL SISTEMA: {resultado['recomendacion']}
NIVEL DE RIESGO GENERAL: {resultado['nivel_riesgo']}

SCORES POR CATEGORÍA:
{lineas_scores}

DIAGNÓSTICO AUTOMÁTICO GENERAL:
{resultado['diagnostico']}

ALERTAS DETECTADAS POR EL SISTEMA:
{lineas_alertas}

RIESGOS INDIVIDUALES REGISTRADOS:
{lineas_riesgos}

Con esta información, escribe un análisis ejecutivo en español que incluya:

1. Un resumen ejecutivo de 2-3 párrafos sobre la viabilidad general del negocio.
2. Los 3 patrones o cruces más importantes entre categorías (por ejemplo, un \
mercado fuerte combinado con finanzas débiles, o un producto sólido pero con \
riesgo competitivo alto) — cosas que el análisis por categoría separada no deja ver.
3. Las 3 principales fortalezas del negocio en su conjunto.
4. Los 3 principales riesgos u obstáculos que podrían impedir su éxito.
5. Entre 3 y 5 recomendaciones estratégicas concretas y accionables, priorizadas \
por lo urgentes o importantes que sean.

Sé directo y específico — evita generalidades como "mejorar el marketing" sin decir \
cómo. Usa un tono profesional pero claro, como si le hablaras directamente al \
dueño del negocio."""

    return prompt


def _generar_con_anthropic(prompt, api_key):

    from anthropic import Anthropic

    cliente = Anthropic(api_key=api_key)

    def _llamada():
        mensaje = cliente.messages.create(
            model=MODELO_ANTHROPIC,
            max_tokens=1800,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return mensaje.content[0].text

    return _con_reintentos(_llamada)


def _generar_con_gemini(prompt, api_key):

    from google import genai

    cliente = genai.Client(api_key=api_key)

    def _llamada():
        respuesta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=prompt
        )
        return respuesta.text

    return _con_reintentos(_llamada)


def generar_analisis_ia(
    resultado,
    riesgos_detalle=None,
    api_key=None,
    proveedor="gemini"
):
    """
    Llama a la IA (Anthropic o Gemini, según 'proveedor') con los
    resultados ya calculados por los engines y devuelve un análisis
    ejecutivo en texto.

    Lanza una excepción si la llamada falla (API key inválida,
    sin conexión, cuota agotada, etc.) — quien llame a esta función
    debe manejar el error y mostrarlo de forma amigable en la UI.
    """

    if not api_key:
        raise ValueError(
            f"No se encontró una API key de {proveedor} configurada."
        )

    prompt = _construir_prompt(resultado, riesgos_detalle)

    if proveedor == "anthropic":
        return _generar_con_anthropic(prompt, api_key)

    elif proveedor == "gemini":
        return _generar_con_gemini(prompt, api_key)

    else:
        raise ValueError(
            f"Proveedor de IA desconocido: '{proveedor}'. "
            "Usa 'anthropic' o 'gemini'."
        )