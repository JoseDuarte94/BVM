# ==========================================
# BVM CHAT ENGINE
#
# Maneja una conversación con la IA donde el
# usuario describe su negocio en lenguaje
# natural + le da los datos financieros, y la
# IA:
#
# 1. Estima los ~35 valores cualitativos (0-100)
#    que normalmente se llenan a mano con los
#    sliders de "Nuevo análisis" (necesidad,
#    diferenciación, confianza, etc.), basándose
#    en la descripción del negocio.
#
# 2. NUNCA inventa los datos financieros ni los
#    datos "duros" de mercado (población, ventas
#    estimadas, crecimiento) — si el usuario no
#    los ha dado, la IA se detiene y los pide
#    explícitamente en el chat.
#
# 3. Cuando ya tiene todo lo necesario, devuelve
#    un bloque JSON con la estructura exacta que
#    esperan los 8 engines de bvm, envuelto en
#    ```json_negocio ... ```.
#
# Este módulo NO corre los engines ni guarda nada
# en la base de datos — solo conversa y extrae los
# datos. Quien llame a esta función se encarga de
# correr los engines con esos datos y mostrarle al
# usuario una vista previa antes de guardar.
# ==========================================

import json
import re
import time


SISTEMA_PROMPT = """Eres un asistente que ayuda a preparar el análisis de un \
modelo de negocio (BVM - Business Validation Model) a partir de una conversación \
con el usuario, en español.

El BVM evalúa un negocio en 8 categorías, cada una con varios factores puntuados \
de 0 a 100 (excepto Finanzas, que usa cifras reales):

MERCADO:
- poblacion (número entero, población del área de mercado)
- porcentaje_objetivo (0-100, % de esa población que es mercado objetivo)
- frecuencia_compra (número, veces que un cliente compra por mes)
- ventas_estimadas (número entero, unidades vendidas estimadas por mes)
- crecimiento (número, % de crecimiento anual estimado del mercado)
- accesibilidad (0-100, qué tan accesible es ese mercado)

PRODUCTO: necesidad, valor_percibido, diferenciacion, calidad, innovacion, \
sustitucion (todos 0-100)

CLIENTE: definicion_cliente, necesidad, capacidad_pago, accesibilidad, \
frecuencia, tamano_segmento (todos 0-100)

ACEPTACION: intencion, relevancia, disposicion_pago, confianza, \
facilidad_compra, barreras (todos 0-100)

COMPETENCIA: competencia_directa, cantidad_competidores, intensidad, \
ventajas_competidores, barreras_entrada, diferenciacion (todos 0-100)

POSICIONAMIENTO: claridad_marca, propuesta_valor, diferenciacion, \
posicionamiento_precio, reconocimiento, coherencia (todos 0-100)

FINANZAS (cifras reales, no 0-100):
- inversion_inicial (monto de inversión inicial)
- precio_venta (precio de venta por unidad)
- unidades_mensuales (unidades vendidas estimadas por mes)
- costo_variable (costo variable por unidad)
- costos_fijos (costos fijos mensuales)

RIESGOS: una lista de riesgos identificados, cada uno con:
- riesgo (nombre corto del riesgo)
- area (una de: Mercado, Producto, Cliente, Competencia, Posicionamiento, \
Finanzas, Operación, Legal, Otro)
- probabilidad (1-5)
- impacto (1-5)

REGLAS IMPORTANTES:

1. Los valores 0-100 de Producto, Cliente, Aceptación, Competencia y \
Posicionamiento, TÚ los estimas a partir de lo que el usuario te describa sobre \
su negocio y tu propio conocimiento del sector — NO se los preguntes uno por uno, \
eso sería agotador para el usuario. Usa buen juicio y sé razonable, ni demasiado \
optimista ni demasiado pesimista.

2. Los datos financieros (inversion_inicial, precio_venta, unidades_mensuales, \
costo_variable, costos_fijos) y los datos "duros" de mercado (poblacion, \
ventas_estimadas, crecimiento) NUNCA los inventes. Si el usuario no te los ha \
dado todavía, PREGÚNTALOS explícitamente y de forma clara (puedes pedir varios \
a la vez). No generes el bloque JSON final hasta tener estos datos.

3. porcentaje_objetivo, frecuencia_compra y accesibilidad (de mercado) sí puedes \
estimarlos razonablemente si el usuario no los da, ya que son más subjetivos.

4. Identifica entre 2 y 5 riesgos razonables para ese tipo de negocio con su \
propia probabilidad e impacto — el usuario los podrá revisar y editar después.

5. Ve conversando de forma natural — puedes hacer preguntas de seguimiento para \
entender mejor el negocio antes de pedir los datos financieros, o pedirlos de una \
vez si el usuario ya dio una descripción completa.

6. SOLO cuando tengas TODO lo necesario (la descripción del negocio, y todos los \
datos financieros y de mercado duros), responde con un breve resumen de lo que \
entendiste y, al final de tu respuesta, agrega un bloque de código con esta \
etiqueta exacta y el JSON completo dentro, sin comentarios ni texto adicional \
dentro del bloque:

```json_negocio
{
  "nombre": "...",
  "mercado": {"poblacion": 0, "porcentaje_objetivo": 0, "frecuencia_compra": 0, \
"ventas_estimadas": 0, "crecimiento": 0, "accesibilidad": 0},
  "producto": {"necesidad": 0, "valor_percibido": 0, "diferenciacion": 0, \
"calidad": 0, "innovacion": 0, "sustitucion": 0},
  "cliente": {"definicion_cliente": 0, "necesidad": 0, "capacidad_pago": 0, \
"accesibilidad": 0, "frecuencia": 0, "tamano_segmento": 0},
  "aceptacion": {"intencion": 0, "relevancia": 0, "disposicion_pago": 0, \
"confianza": 0, "facilidad_compra": 0, "barreras": 0},
  "competencia": {"competencia_directa": 0, "cantidad_competidores": 0, \
"intensidad": 0, "ventajas_competidores": 0, "barreras_entrada": 0, \
"diferenciacion": 0},
  "posicionamiento": {"claridad_marca": 0, "propuesta_valor": 0, \
"diferenciacion": 0, "posicionamiento_precio": 0, "reconocimiento": 0, \
"coherencia": 0},
  "finanzas": {"inversion_inicial": 0, "precio_venta": 0, \
"unidades_mensuales": 0, "costo_variable": 0, "costos_fijos": 0},
  "riesgos": [
    {"riesgo": "...", "area": "...", "probabilidad": 1, "impacto": 1}
  ]
}
```

No agregues ese bloque si todavía te falta información — en ese caso, solo \
sigue conversando y pidiendo lo que falta."""


def _extraer_json(texto):
    """
    Busca un bloque ```json_negocio ... ``` en el texto de la IA.
    Devuelve el dict parseado, o None si no hay bloque o no es
    JSON válido (en cuyo caso se sigue conversando normalmente).
    """

    patron = r"```json_negocio\s*(\{.*?\})\s*```"

    coincidencia = re.search(patron, texto, re.DOTALL)

    if not coincidencia:
        return None

    try:
        return json.loads(coincidencia.group(1))
    except json.JSONDecodeError:
        return None


def _quitar_bloque_json(texto):
    """
    Quita el bloque ```json_negocio ... ``` del texto para no
    mostrárselo crudo al usuario en el chat.
    """

    patron = r"```json_negocio\s*\{.*?\}\s*```"

    return re.sub(patron, "", texto, flags=re.DOTALL).strip()


def _historial_para_anthropic(historial):

    return [
        {"role": mensaje["role"], "content": mensaje["content"]}
        for mensaje in historial
    ]


def _historial_para_gemini(historial):

    contenidos = []

    for mensaje in historial:

        rol = "model" if mensaje["role"] == "assistant" else "user"

        contenidos.append({
            "role": rol,
            "parts": [{"text": mensaje["content"]}]
        })

    return contenidos


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
    Ejecuta 'funcion' (sin argumentos, usar una lambda o closure)
    reintentando con espera progresiva (5s, 10s, 20s...) solo si
    el error parece temporal (servidor saturado o límite por
    minuto). Con los valores por defecto, espera hasta 35s en
    total antes de rendirse. Si se agotan los intentos, o el
    error no es temporal, se relanza la excepción original tal
    cual.
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


def _enviar_con_anthropic(historial, api_key, modelo):

    from anthropic import Anthropic

    cliente = Anthropic(api_key=api_key)

    def _llamada():

        mensaje = cliente.messages.create(
            model=modelo,
            max_tokens=2000,
            system=SISTEMA_PROMPT,
            messages=_historial_para_anthropic(historial)
        )

        return mensaje.content[0].text

    return _con_reintentos(_llamada)


def _enviar_con_gemini(historial, api_key, modelo):

    from google import genai
    from google.genai import types

    cliente = genai.Client(api_key=api_key)

    def _llamada():

        respuesta = cliente.models.generate_content(
            model=modelo,
            contents=_historial_para_gemini(historial),
            config=types.GenerateContentConfig(
                system_instruction=SISTEMA_PROMPT
            )
        )

        return respuesta.text

    return _con_reintentos(_llamada)


def enviar_mensaje_chat(
    historial,
    api_key,
    proveedor="gemini",
    modelo_anthropic="claude-sonnet-5",
    modelo_gemini="gemini-3.6-flash"
):
    """
    historial: lista de dicts [{"role": "user"|"assistant", "content": str}, ...]
    (el último elemento debe ser el mensaje del usuario que se quiere responder)

    Devuelve una tupla (texto_para_mostrar, datos_json_o_none, fuentes):
    - texto_para_mostrar: la respuesta de la IA, sin el bloque JSON crudo.
    - datos_json_o_none: el dict estructurado si la IA ya reunió todo lo
      necesario, o None si todavía sigue conversando.
    - fuentes: siempre una lista vacía (ya no se usa búsqueda web) — se
      mantiene en la firma de la función para no tener que tocar app4.py.
    """

    if proveedor == "anthropic":
        texto_crudo = _enviar_con_anthropic(historial, api_key, modelo_anthropic)

    elif proveedor == "gemini":
        texto_crudo = _enviar_con_gemini(historial, api_key, modelo_gemini)

    else:
        raise ValueError(
            f"Proveedor de IA desconocido: '{proveedor}'. "
            "Usa 'anthropic' o 'gemini'."
        )

    datos = _extraer_json(texto_crudo)

    texto_limpio = _quitar_bloque_json(texto_crudo)

    return texto_limpio, datos, []