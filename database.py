"""
SEGRIMSA - Base de Datos para Streamlit Cloud
Solo las tablas necesarias para el formulario de registro.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "segrimsa.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_catequesis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_padre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT,
            nombre_nino TEXT NOT NULL,
            colegio TEXT NOT NULL,
            grado TEXT NOT NULL,
            tiene_hermano INTEGER DEFAULT 0,
            hermano1_nombre TEXT,
            hermano1_colegio TEXT,
            hermano1_grado TEXT,
            hermano2_nombre TEXT,
            hermano2_colegio TEXT,
            hermano2_grado TEXT,
            evento TEXT,
            parroquia TEXT,
            sacramento TEXT,
            anio INTEGER,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notas TEXT
        )
    """)

    conn.commit()
    conn.close()
