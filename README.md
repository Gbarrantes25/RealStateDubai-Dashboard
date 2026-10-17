# Real Estate Dubai Dashboard 🏙️

## 📃 Descripción General
Proyecto de análisis y visualización del mercado inmobiliario de Dubái, desarrollado en Python con **marimo** y **Plotly**, diseñado para explorar la evolución histórica de los precios, el valor de ventas y el volumen de transacciones por área, tipo de propiedad, tipo de registro y uso autorizado.

Este proyecto transforma un dataset de transacciones de venta (`dld_sales_transactions.parquet`) en un notebook interactivo mediante:
- 🧹 **Limpieza y Transformación de Datos**: selección de columnas relevantes, imputación del precio por m² a partir del valor de venta (`price_aed / 10764`), eliminación de registros sin área o sin nombre de área, relleno de subtipos faltantes con `Unknown`, renombrado de columnas al español, conversión de fechas a periodo anual y tipado `category` para variables categóricas.
- 📈 **Agrupaciones y Métricas**: medianas de precio por m², sumas de valor de venta, conteo de transacciones, variación porcentual año contra año (YoY) y crecimiento del precio por m² en los últimos 5 años.
- 📊 **Visualizaciones Estadísticas**: series de tiempo, barras, gráfico de Pareto (regla 80/20), rankings Top N, heatmaps de correlación y comparativos Residencial vs Comercial.
- 🖱️ **Filtros Interactivos**: selectores de área, tipo de registro y año mediante widgets de marimo (`mo.ui.dropdown`) con tarjetas de métricas (`mo.stat`).

## 📊 Contenido del proyecto
El notebook responde 12 preguntas de negocio, cada una con su visualización y una sección desplegable de **Hallazgos**:

1. Tendencia histórica del precio por m² en cada área.
2. Tendencia histórica del precio de venta por tipo de registro (Ready / Off-Plan).
3. Tendencia histórica del precio por m² por tipo de propiedad (Villa, Land, Building, Unit).
4. Tendencia histórica del precio de venta por tipo de uso autorizado (Residential, Commercial, Other).
5. Variación porcentual de los últimos 5 años del precio de venta por tipo de registro.
6. Áreas que concentran el 80% de las ventas del año seleccionado (Pareto).
7. Ranking de áreas que superan la media del precio por m² del año seleccionado.
8. Evolución del volumen de transacciones por año y por tipo de propiedad.
9. Ranking de las 15 áreas con mayor crecimiento del precio por m² en los últimos 5 años.
10. Relación entre tamaño (m²) y precio de venta / precio por m² por tipo de propiedad (heatmaps de correlación).
11. Distribución del precio por m² por tipo de propiedad en los últimos 3 años.
12. Comparación Residencial vs Comercial: precio medio por m² y volumen de transacciones a lo largo del tiempo.

## 🛠️ Herramientas y Tecnologías Utilizadas
- Desarrollo y Visualización: Python, marimo, Plotly.
- Librerías:
  - `pandas` y `numpy` para manipulación, limpieza y agregación de datos.
  - `plotly` (`graph_objects` y `subplots`) para gráficos interactivos.
  - `marimo` para el notebook reactivo, widgets y despliegue como app.
- Fuente de Datos: transacciones de venta inmobiliaria de Dubái, almacenadas en formato `.parquet`.
- Gestor de Entorno: UV.
- Despliegue: [molab (marimo)](https://molab.marimo.io/notebooks/nb_uZDGMLYu2AM41RZHYwq6ut/app).

## ⚙️ Configuración del Entorno
- Software Necesario: Python (versión definida en `.python-version`) y las librerías `marimo`, `pandas`, `numpy` y `plotly`.
- Instalación:
  - Clonar el repositorio.
  - Instalar dependencias con UV: `uv sync`.
  - Ejecutar como aplicación: `marimo run app.py`.
  - Editar el notebook: `marimo edit app.py`.

## 📂 Estructura del Repositorio
```text
.
├── app.py                           # Notebook marimo con el análisis y las visualizaciones
├── README.md                        # Este archivo
├── dld_sales_transactions.parquet   # Dataset de transacciones de venta
├── uv.lock                          # Gestor de paquetes del proyecto
├── pyproject.toml                   # Gestor y configuración de dependencias
└── python-version                   # Versión de Python del proyecto
```

## ✅ Características Principales
- Notebook reactivo con marimo, desplegado como app web interactiva.
- Optimización de Rendimiento:
  - `@mo.cache()` para evitar recargar el dataset en cada interacción.
  - Funciones modulares por gráfico, que se recalculan solo cuando cambia su filtro.
- Filtros por área, tipo de registro y año.
- Gráfico de Pareto para identificar las áreas que concentran el 80% de las ventas.
- Rankings de áreas por precio por m² y por crecimiento en los últimos 5 años.
- Heatmaps de correlación entre m², valor de venta y precio por m² por tipo de propiedad.
- Hallazgos contextualizados en acordeones desplegables bajo cada visualización.

## 🔎 Algunos Hallazgos
- El uso Residencial supera ampliamente en ventas a las demás categorías de uso autorizado.
- Villa y Building muestran un crecimiento acelerado del precio por m² en los últimos 5 años, mientras que Land y Unit se mantienen.
- Solo cerca del 14% de las áreas concentra el 80% de las ventas.
- El número de áreas que superan la media del precio por m² pasó de 37 (2022) a 64 (2026).
- Las 15 áreas con mayor crecimiento han al menos triplicado su precio por m² en 5 años.

## 🖼️ Vistas Previas del proyecto
<details>
  <summary>Dashboard</summary>

  <!-- Agrega aquí tus capturas de pantalla -->

</details>

## 👤 Autor
- Giancarlo Barrantes
- Lima, Perú
- [Linkedin](https://www.linkedin.com/in/gb25/)
