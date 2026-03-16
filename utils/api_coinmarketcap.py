# Importar requests para hacer peticiones HTTP
import requests

# Importar la API KEY
from config import API_KEY


# Función para convertir criptomonedas
def convertir_moneda(moneda_from, moneda_to, cantidad):
    """
    Consultar la API de CoinMarketCap para convertir monedas
    """

    # Definir URL del endpoint
    url = "https://pro-api.coinmarketcap.com/v2/tools/price-conversion"

    # Definir parámetros de la consulta
    params = {
        "symbol": moneda_from,
        "convert": moneda_to,
        "amount": cantidad
    }

    # Definir cabeceras con la API key
    headers = {
        "X-CMC_PRO_API_KEY": API_KEY
    }

    # Enviar petición a la API
    response = requests.get(url, headers=headers, params=params)

    # Convertir respuesta a JSON
    data = response.json()

    # Obtener el resultado de la conversión
    resultado = data["data"][0]["quote"][moneda_to]["price"]

    return resultado