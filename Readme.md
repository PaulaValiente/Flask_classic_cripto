# CriptoMovimientos

CriptoCambio es una aplicación web desarrollada con **Python y Flask** que permite registrar operaciones de compra, venta e intercambio de criptomonedas y calcular el estado actual de la inversión.

La aplicación guarda todas las operaciones en una base de datos SQLite y consulta el valor real de las criptomonedas mediante la **API de CoinMarketCap**.

---

# Objetivo de la aplicación

El objetivo de la aplicación es simular una pequeña cartera de criptomonedas donde el usuario puede:

- comprar criptomonedas con euros
- vender criptomonedas por euros
- intercambiar criptomonedas entre sí
- registrar todas las operaciones
- consultar el estado actual de su inversión

---

# Tecnologías utilizadas

La aplicación está desarrollada utilizando:

- Python
- Flask
- SQLite
- HTML
- Jinja2
- CoinMarketCap API

---

# Desarrollo del proyecto

El desarrollo de la aplicación se ha realizado por fases.

---

# Fase 1 – Creación de la estructura del proyecto

Se creó la estructura inicial del proyecto Flask con las carpetas principales.

También se crearon los archivos principales.
---

# Fase 2 – Creación de la base de datos

Se creó una base de datos SQLite.

# Fase 3 – Creación de la aplicación Flask

En `app.py` se creó la aplicación Flask y las rutas principales.

# Fase 4 – Creación de la plantilla base

Se creó `base.html` para definir la estructura común de la aplicación.

Las demás páginas heredan esta plantilla utilizando **Jinja2**.

---

# Fase 5 – Creación del formulario de operaciones

En `purchase.html` se creó un formulario.

# Fase 6 – Conexión con la API de CoinMarketCap

Se creó el archivo: utils/api_coinmarketcap.py


para consultar el valor actual de las criptomonedas utilizando la API de CoinMarketCap.

Esto permite calcular el valor de conversión entre monedas.

---

# Fase 7 – Guardar operaciones en la base de datos

Cuando el usuario confirma una operación, los movimientos se muestran en la página **Inicio**.

---

# Fase 8 – Validación del saldo

Se añadió una validación para evitar vender más criptomonedas de las que se tienen.

---

# Fase 9 – Cálculo del estado de la inversión

En la página **Estado** se calculan los valores principales de la inversión:

- invertido
- recuperado
- valor de compra
- valor actual

---

# Fase 10 – Cálculo de ganancia o pérdida

Se calcula el resultado final de la inversión:

Si el resultado es positivo se muestra **ganancia**.

Si es negativo se muestra **pérdida**.

---

# Mejoras finales

Se realizaron varias mejoras para mejorar la presentación:

- mostrar números con **2 decimales**
- utilizar **coma decimal** en lugar de punto
- mostrar la **cartera actual de criptomonedas**
- mostrar resultados con colores

# Ejecución de la aplicación

- Activar el entorno virtual
- Instalar dependencias
- Ejecutar aplicación 