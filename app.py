# Importar Flask
from flask import Flask, render_template, request

# Importar funciones de base de datos
from database import (
    create_table,
    get_movimientos,
    insert_movimiento,
    get_saldo,
    get_invertido,
    get_recuperado
)

# Importar función de conversión
from utils.api_coinmarketcap import convertir_moneda

# Importar datetime
from datetime import datetime


# Crear aplicación Flask
app = Flask(__name__)

# Crear tabla si no existe
create_table()


# -------------------------------
# RUTA PRINCIPAL
# -------------------------------

@app.route("/")
def index():
    """
    Mostrar movimientos registrados
    """

    movimientos = get_movimientos()

    return render_template("index.html", movimientos=movimientos)


# -------------------------------
# RUTA PURCHASE
# -------------------------------

@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    """
    Mostrar formulario y procesar operaciones
    """

    resultado = None
    error = None

    if request.method == "POST":

        moneda_from = request.form["from"]
        moneda_to = request.form["to"]
        cantidad = float(request.form["cantidad"])
        accion = request.form["action"]

        # Calcular conversión
        resultado = convertir_moneda(moneda_from, moneda_to, cantidad)

        if accion == "aceptar":

            # Validar saldo si no es EUR
            if moneda_from != "EUR":

                saldo = get_saldo(moneda_from)

                if cantidad > saldo:
                    error = "No tienes suficiente saldo"
                    return render_template("purchase.html", resultado=resultado, error=error)

            # Obtener fecha actual
            fecha = datetime.now().strftime("%Y-%m-%d")

            # Obtener hora actual
            hora = datetime.now().strftime("%H:%M:%S")

            # Guardar movimiento
            insert_movimiento(
                fecha,
                hora,
                moneda_from,
                cantidad,
                moneda_to,
                resultado
            )

    return render_template("purchase.html", resultado=resultado, error=error)


# -------------------------------
# RUTA STATUS
# -------------------------------

@app.route("/status")
def status():
    """
    Calcular estado de la inversión
    """

    # Obtener total invertido
    invertido = get_invertido()

    # Obtener total recuperado
    recuperado = get_recuperado()

    # Calcular valor de compra
    valor_compra = invertido - recuperado

    criptos = ["BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"]

    valor_actual = 0

    cartera = {}

    # Calcular saldo y valor de cada cripto
    for cripto in criptos:

        saldo = get_saldo(cripto)

        if saldo > 0:

            cartera[cripto] = saldo

            euros = convertir_moneda(cripto, "EUR", saldo)

            valor_actual += euros

    # Redondear valores
    valor_actual = round(valor_actual, 2)
    valor_compra = round(valor_compra, 2)
    invertido = round(invertido, 2)
    recuperado = round(recuperado, 2)

    # Calcular ganancia
    ganancia = round(valor_actual - valor_compra, 2)

    return render_template(
        "status.html",
        invertido=invertido,
        recuperado=recuperado,
        valor_compra=valor_compra,
        valor_actual=valor_actual,
        ganancia=ganancia,
        cartera=cartera
    )
# -------------------------------
# EJECUTAR APP
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)