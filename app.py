from flask import Flask, render_template, request
from datetime import datetime

# Importar funciones de base de datos
from database import create_table, insert_movimiento, get_movimientos, get_saldo

# Importar funciones de API
from utils.api_coinmarketcap import convertir, get_monedas

# Crear aplicación Flask
app = Flask(__name__)

# Crear tabla si no existe
create_table()

# Crear filtro para formatear números a formato europeo
def formato_euro(valor):
    try:
        # Formatear a 2 decimales y convertir punto en coma
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        # Devolver valor sin modificar si hay error
        return valor

# Registrar filtro en Jinja
app.jinja_env.filters["euro"] = formato_euro


# Ruta principal para mostrar historial
@app.route("/")
def index():
    # Obtener movimientos de la base de datos
    movimientos = get_movimientos()
    
    # Renderizar plantilla index
    return render_template("index.html", movimientos=movimientos)


# Ruta para realizar compra/venta
@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    # Obtener listado de monedas
    monedas = get_monedas()
    
    # Inicializar variables
    cantidad_to = None
    error = None

    # Comprobar si la petición es POST
    if request.method == "POST":
        
        # Obtener datos del formulario
        moneda_from = request.form.get("coin_from")
        moneda_to = request.form.get("coin_to")
        accion = request.form.get("action")

        # Validar cantidad introducida
        try:
            cantidad_from = float(request.form.get("cantidad"))
        except:
            error = "Cantidad inválida"
            return render_template("purchase.html", monedas=monedas, error=error)

        # Validar que las monedas sean distintas
        if moneda_from == moneda_to:
            error = "No se puede convertir la misma moneda"
            return render_template("purchase.html", monedas=monedas, error=error)

        # Validar saldo si no es EUR
        if moneda_from != "EUR":
            saldo = get_saldo(moneda_from)
            if cantidad_from > saldo:
                error = "Saldo insuficiente"
                return render_template("purchase.html", monedas=monedas, error=error)

        # Realizar conversión usando API
        precio = convertir(moneda_from, moneda_to, cantidad_from)

        # Comprobar error en API
        if precio is None:
            error = "Error en API"
            return render_template("purchase.html", monedas=monedas, error=error)

        # Guardar resultado de conversión
        cantidad_to = precio

        # Guardar operación solo si se confirma
        if accion == "confirmar":
            now = datetime.now()

            insert_movimiento(
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                moneda_from,
                cantidad_from,
                moneda_to,
                cantidad_to
            )

            return render_template("purchase.html", monedas=monedas, cantidad_to=cantidad_to)

    # Renderizar plantilla
    return render_template("purchase.html", monedas=monedas, cantidad_to=cantidad_to, error=error)


# Ruta para mostrar estado de inversión
@app.route("/status")
def status():
    # Obtener monedas disponibles
    monedas = get_monedas()

    # Crear cartera
    cartera = {}
    for m in monedas:
        if m != "EUR":
            saldo = get_saldo(m)
            if saldo != 0:
                cartera[m] = saldo

    # Obtener saldo en EUR
    saldo_eur = get_saldo("EUR")

    # Calcular invertido y recuperado
    invertido = -saldo_eur if saldo_eur < 0 else 0
    recuperado = saldo_eur if saldo_eur > 0 else 0

    # Calcular valor de compra
    valor_compra = invertido - recuperado

    # Calcular valor actual de la cartera
    valor_actual = 0
    for cripto, cantidad in cartera.items():
        precio = convertir(cripto, "EUR", 1)
        if precio:
            valor_actual += cantidad * precio

    # Calcular ganancia o pérdida
    ganancia = valor_actual - valor_compra

    # Renderizar plantilla status
    return render_template(
        "status.html",
        invertido=invertido,
        recuperado=recuperado,
        valor_compra=valor_compra,
        valor_actual=valor_actual,
        ganancia=ganancia,
        cartera=cartera
    )


# Ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)