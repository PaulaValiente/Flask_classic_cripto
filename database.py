import sqlite3
from pathlib import Path

# Definir ruta de la base de datos y crear carpeta si no existe
DB_PATH = Path("instance/movimientos.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    # Crear conexión a la base de datos
    conn = sqlite3.connect(DB_PATH)
    
    # Permitir acceder a columnas por nombre
    conn.row_factory = sqlite3.Row
    
    return conn

def create_table():
    # Crear tabla de movimientos si no existe
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            moneda_from TEXT NOT NULL,
            cantidad_from REAL NOT NULL,
            moneda_to TEXT NOT NULL,
            cantidad_to REAL NOT NULL
        )
        """)

def insert_movimiento(date, time, moneda_from, cantidad_from, moneda_to, cantidad_to):
    # Insertar un nuevo movimiento en la base de datos
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to))

def get_movimientos():
    # Obtener todos los movimientos ordenados por id descendente
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM movimientos ORDER BY id DESC")
        return cursor.fetchall()

def get_saldo(moneda):
    # Calcular saldo de una moneda
    
    with get_connection() as conn:
        cursor = conn.cursor()

        # Obtener total enviado (from)
        cursor.execute("SELECT SUM(cantidad_from) FROM movimientos WHERE moneda_from = ?", (moneda,))
        suma_from = cursor.fetchone()[0]

        # Obtener total recibido (to)
        cursor.execute("SELECT SUM(cantidad_to) FROM movimientos WHERE moneda_to = ?", (moneda,))
        suma_to = cursor.fetchone()[0]

        # Evitar valores None
        suma_from = suma_from or 0
        suma_to = suma_to or 0

        # Calcular saldo final
        return suma_to - suma_from