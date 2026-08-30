# ==========================================
# BVM DATABASE
# V2.3
# ==========================================

import sqlite3


DATABASE = "bvm.db"


# ------------------------------------------
# CONECTAR
# ------------------------------------------

def conectar():

    conexion = sqlite3.connect(DATABASE)

    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


# ------------------------------------------
# CREAR TABLAS
# ------------------------------------------

def inicializar_base_datos():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS negocios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            mercado REAL,
            producto REAL,
            cliente REAL,
            aceptacion REAL,
            competencia REAL,
            posicionamiento REAL,
            finanzas REAL,
            riesgo REAL,

            business_score REAL,

            recomendacion TEXT,

            nivel_riesgo TEXT,

            diagnostico TEXT
        )
    """)

    # ======================================
    # TABLA DE DETALLE DE RIESGOS
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS riesgos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            negocio_id INTEGER NOT NULL,

            riesgo TEXT,
            area TEXT,

            probabilidad INTEGER,
            impacto INTEGER,
            nivel INTEGER,

            clasificacion TEXT,
            accion TEXT,

            FOREIGN KEY (negocio_id)
                REFERENCES negocios (id)
                ON DELETE CASCADE
        )
    """)

    # ======================================
    # MIGRACIÓN: columna analisis_ia
    #
    # Si la tabla 'negocios' ya existía de antes
    # (creada por una versión anterior de la app),
    # CREATE TABLE IF NOT EXISTS no la modifica.
    # Por eso aquí revisamos si falta la columna
    # 'analisis_ia' y la agregamos manualmente.
    # ======================================

    columnas = cursor.execute(
        "PRAGMA table_info(negocios)"
    ).fetchall()

    nombres_columnas = [columna[1] for columna in columnas]

    if "analisis_ia" not in nombres_columnas:

        cursor.execute(
            "ALTER TABLE negocios ADD COLUMN analisis_ia TEXT"
        )

    conexion.commit()

    conexion.close()


# ------------------------------------------
# GUARDAR NEGOCIO
# ------------------------------------------

def guardar_negocio(resultado, riesgos_detalle=None):
    """
    Guarda el negocio analizado y, si se provee,
    el detalle de cada riesgo identificado
    (típicamente resultado_riesgo["riesgos"]
    devuelto por risk_engine.calcular_risk_score).
    """

    conexion = conectar()

    cursor = conexion.cursor()

    scores = resultado["scores"]

    cursor.execute("""
        INSERT INTO negocios (

            nombre,

            mercado,
            producto,
            cliente,
            aceptacion,
            competencia,
            posicionamiento,
            finanzas,
            riesgo,

            business_score,

            recomendacion,

            nivel_riesgo,

            diagnostico

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        resultado["nombre"],

        scores["mercado"],
        scores["producto"],
        scores["cliente"],
        scores["aceptacion"],
        scores["competencia"],
        scores["posicionamiento"],
        scores["finanzas"],
        scores["riesgo"],

        resultado["business_score"],

        resultado["recomendacion"],

        resultado["nivel_riesgo"],

        resultado["diagnostico"]

    ))

    negocio_id = cursor.lastrowid

    # ======================================
    # GUARDAR DETALLE DE RIESGOS
    # ======================================

    if riesgos_detalle:

        for riesgo_item in riesgos_detalle:

            cursor.execute("""
                INSERT INTO riesgos (

                    negocio_id,

                    riesgo,
                    area,

                    probabilidad,
                    impacto,
                    nivel,

                    clasificacion,
                    accion

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """, (

                negocio_id,

                riesgo_item["riesgo"],
                riesgo_item["area"],

                riesgo_item["probabilidad"],
                riesgo_item["impacto"],
                riesgo_item["nivel"],

                riesgo_item["clasificacion"],
                riesgo_item["accion"]

            ))

    conexion.commit()

    conexion.close()

    return negocio_id


# ------------------------------------------
# OBTENER NEGOCIOS
# ------------------------------------------

def obtener_negocios():
    """
    Devuelve todos los negocios guardados con TODAS sus
    columnas, en el mismo orden en que están definidas en
    la tabla 'negocios':

    0  id
    1  nombre
    2  mercado
    3  producto
    4  cliente
    5  aceptacion
    6  competencia
    7  posicionamiento
    8  finanzas
    9  riesgo
    10 business_score
    11 recomendacion
    12 nivel_riesgo
    13 diagnostico
    """

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            mercado,
            producto,
            cliente,
            aceptacion,
            competencia,
            posicionamiento,
            finanzas,
            riesgo,
            business_score,
            recomendacion,
            nivel_riesgo,
            diagnostico
        FROM negocios
        ORDER BY business_score DESC
    """)

    negocios = cursor.fetchall()

    conexion.close()

    return negocios


# ------------------------------------------
# OBTENER RIESGOS DE UN NEGOCIO
# ------------------------------------------

def obtener_riesgos_por_negocio(negocio_id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            riesgo,
            area,
            probabilidad,
            impacto,
            nivel,
            clasificacion,
            accion
        FROM riesgos
        WHERE negocio_id = ?
        ORDER BY nivel DESC
    """, (negocio_id,))

    riesgos = cursor.fetchall()

    conexion.close()

    return riesgos


# ------------------------------------------
# GUARDAR ANÁLISIS DE IA
# ------------------------------------------

def guardar_analisis_ia(negocio_id, texto):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE negocios SET analisis_ia = ? WHERE id = ?",
        (texto, negocio_id)
    )

    conexion.commit()

    conexion.close()


# ------------------------------------------
# OBTENER ANÁLISIS DE IA
# ------------------------------------------

def obtener_analisis_ia(negocio_id):

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT analisis_ia FROM negocios WHERE id = ?",
        (negocio_id,)
    )

    fila = cursor.fetchone()

    conexion.close()

    return fila[0] if fila else None


# ------------------------------------------
# ELIMINAR NEGOCIO
# ------------------------------------------

def eliminar_negocio(negocio_id):
    """
    Elimina un negocio guardado. Gracias a
    ON DELETE CASCADE, sus riesgos asociados
    en la tabla 'riesgos' se eliminan también.
    """

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM negocios WHERE id = ?",
        (negocio_id,)
    )

    conexion.commit()

    conexion.close()

