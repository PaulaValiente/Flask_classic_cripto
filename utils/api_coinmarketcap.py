import requests
from config import API_KEY

URL_CONVERT = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion"
URL_MAP = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"


def convertir(coin_from, coin_to, cantidad):
    """
    Convertir una cantidad de una moneda a otra usando la API
    """

    headers = {
        "X-CMC_PRO_API_KEY": API_KEY
    }

    params = {
        "amount": float(cantidad),
        "symbol": coin_from,
        "convert": coin_to
    }

    try:
        response = requests.get(URL_CONVERT, headers=headers, params=params)

        if response.status_code != 200:
            print("ERROR API:", response.text)
            return None

        data = response.json()

        return data.get("data", {}).get("quote", {}).get(coin_to, {}).get("price")

    except Exception as e:
        print("ERROR:", e)
        return None


def get_monedas():
    """
    Obtener listado de monedas desde la API
    """

    headers = {
        "X-CMC_PRO_API_KEY": API_KEY
    }

    try:
        response = requests.get(URL_MAP, headers=headers)

        if response.status_code != 200:
            print("ERROR API:", response.text)
            return []

        data = response.json()

        monedas = [item["symbol"] for item in data.get("data", [])]

        # Añadir EUR manualmente
        monedas = ["EUR"] + monedas

        return monedas[:20]

    except Exception as e:
        print("ERROR:", e)
        return []