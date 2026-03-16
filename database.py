# Importar sqlite3 para trabajar con la base de datos
import sqlite3


# Definir ruta de la base de datos
DATABASE = "instance/movimientos.db"


# -------------------------------
# CREAR CONEXIÓN A LA BASE DE DATOS
# -------------------------------

def get_connection():
    """
    Crear conexión con la base de datos SQLite
    """

    # Conectar a la base de datos
    conn = sqlite3.connect(DATABASE)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    # Devolver la conexión
    return conn


# -------------------------------
# CREAR TABLA MOVIMIENTOS
# -------------------------------

def create_table():
    """
    Crear tabla movimientos si no existe
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            moneda_from TEXT,
            cantidad_from REAL,
            moneda_to TEXT,
            cantidad_to REAL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------
# INSERTAR MOVIMIENTO
# -------------------------------

def insert_movimiento(date, time, moneda_from, cantidad_from, moneda_to, cantidad_to):
    """
    Insertar movimiento en la base de datos
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO movimientos
        (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to))

    conn.commit()
    conn.close()


# -------------------------------
# OBTENER MOVIMIENTOS
# -------------------------------

def get_movimientos():
    """
    Obtener todos los movimientos registrados
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM movimientos
        ORDER BY date DESC, time DESC
    """)

    movimientos = cursor.fetchall()

    conn.close()

    return movimientos


# -------------------------------
# CALCULAR SALDO DE UNA MONEDA
# -------------------------------

def get_saldo(moneda):
    """
    Calcular saldo de una criptomoneda
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Calcular suma de monedas obtenidas
    cursor.execute("""
        SELECT SUM(cantidad_to)
        FROM movimientos
        WHERE moneda_to = ?
    """, (moneda,))

    suma_to = cursor.fetchone()[0] or 0

    # Calcular suma de monedas gastadas
    cursor.execute("""
        SELECT SUM(cantidad_from)
        FROM movimientos
        WHERE moneda_from = ?
    """, (moneda,))

    suma_from = cursor.fetchone()[0] or 0

    conn.close()

    # Calcular saldo final
    saldo = suma_to - suma_from

    return saldo


# -------------------------------
# CALCULAR TOTAL INVERTIDO
# -------------------------------

def get_invertido():
    """
    Calcular total de euros invertidos en criptomonedas
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(cantidad_from)
        FROM movimientos
        WHERE moneda_from = 'EUR'
    """)

    invertido = cursor.fetchone()[0] or 0

    conn.close()

    return invertido


# -------------------------------
# CALCULAR TOTAL RECUPERADO
# -------------------------------

def get_recuperado():
    """
    Calcular total de euros recuperados al vender criptos
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(cantidad_to)
        FROM movimientos
        WHERE moneda_to = 'EUR'
    """)

    recuperado = cursor.fetchone()[0] or 0

    conn.close()

    return recuperado