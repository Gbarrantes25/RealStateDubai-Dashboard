# 🏙️ Real Estate Dubai Dashboard

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![marimo](https://img.shields.io/badge/marimo-FFD700?style=flat&logo=python&logoColor=black)](https://marimo.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-blue.svg)]()

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Contenido del Proyecto](#-contenido-del-proyecto)
- [Herramientas y Tecnologías](#️-herramientas-y-tecnologías-utilizadas)
- [Configuración del Entorno](#️-configuración-del-entorno)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Algunos Hallazgos](#-algunos-hallazgos)
- [Vistas Previas](#️-vistas-previas-del-proyecto)
- [Autor](#-autor)
- [Licencia](#-licencia)

---

## 📃 Descripción General

Proyecto de análisis y visualización del **mercado inmobiliario de Dubái**, desarrollado en Python con **marimo** y **Plotly**, diseñado para explorar la evolución histórica de los precios, el valor de ventas y el volumen de transacciones por área, tipo de propiedad, tipo de registro y uso autorizado.

Este proyecto transforma un dataset de transacciones de venta (`dld_sales_transactions.parquet`) en un notebook reactivo e interactivo mediante:

- 🧹 **Limpieza y Transformación de Datos:** Selección de columnas relevantes, cálculo del precio por m² (`price_aed / 10764`), eliminación de registros sin área, relleno de subtipos faltantes con `Unknown`, renombrado de columnas al español, conversión de fechas a periodo anual y tipado `category` para optimizar la memoria.
- 📈 **Agrupaciones y Métricas:** Medianas de precio por m², sumas de valor de venta, conteo de transacciones, variación porcentual año contra año (YoY) y crecimiento del precio por m² en los últimos 5 años.
- 📊 **Visualizaciones Estadísticas:** Series de tiempo, gráficos de barras, gráfico de Pareto (regla 80/20), rankings Top N, heatmaps de correlación y comparativos Residencial vs Comercial.
- 🖱️ **Filtros Interactivos:** Selectores de área, tipo de registro y año mediante widgets reactivos de marimo (`mo.ui.dropdown`) con tarjetas de métricas (`mo.stat`).

---

## ✨ Características Principales

### 🔄 Notebook Reactivo con marimo
- Experiencia de usuario similar a una aplicación web, donde los widgets actualizan solo las celdas dependientes.
- Despliegue sencillo como app web interactiva mediante `molab` (marimo cloud).

### 🚀 Optimización de Rendimiento
- Uso de `@mo.cache()` para evitar recargar y reprocesar el dataset `.parquet` en cada interacción.
- Funciones modulares por gráfico, que se recalculan de forma aislada solo cuando cambia su filtro específico.

### 📐 Análisis Estadístico Avanzado
- Gráfico de Pareto para identificar las áreas que concentran el 80% de las ventas.
- Rankings dinámicos de áreas por precio por m² y por crecimiento en los últimos 5 años.
- Heatmaps de correlación entre tamaño (m²), valor de venta y precio por m² segmentados por tipo de propiedad.
- Hallazgos contextualizados en acordeones desplegables bajo cada visualización.

---

## 📊 Contenido del Proyecto

El notebook responde 12 preguntas de negocio clave, cada una con su visualización y una sección desplegable de **Hallazgos**:

| # | Pregunta de Negocio | Contenido Principal |
|---|---------------------|---------------------|
| **01** | Tendencia histórica del precio por m² en cada área. | Series de tiempo comparativas por zona. |
| **02** | Tendencia histórica del precio de venta por tipo de registro. | Comparativa Ready (listo) vs Off-Plan (en plano). |
| **03** | Tendencia histórica del precio por m² por tipo de propiedad. | Evolución de Villa, Land, Building y Unit. |
| **04** | Tendencia histórica del precio de venta por tipo de uso autorizado. | Desglose Residential, Commercial y Other. |
| **05** | Variación porcentual de los últimos 5 años del precio de venta. | Crecimiento YoY por tipo de registro. |
| **06** | Áreas que concentran el 80% de las ventas del año seleccionado. | Gráfico de Pareto (regla 80/20). |
| **07** | Ranking de áreas que superan la media del precio por m². | Top N de áreas premium por año. |
| **08** | Evolución del volumen de transacciones por año y tipo de propiedad. | Gráficos de barras apiladas o líneas de volumen. |
| **09** | Ranking de las 15 áreas con mayor crecimiento del precio por m². | Top 15 de plusvalía en 5 años. |
| **10** | Relación entre tamaño (m²) y precio de venta / precio por m². | Heatmaps de correlación por tipo de propiedad. |
| **11** | Distribución del precio por m² por tipo de propiedad. | Análisis de distribución en los últimos 3 años. |
| **12** | Comparación Residencial vs Comercial. | Precio medio por m² y volumen de transacciones a lo largo del tiempo. |

---

## 🛠️ Herramientas y Tecnologías Utilizadas

### Software y Lenguajes
- **Python** - Lenguaje de programación principal.
- **marimo** - Notebook reactivo de Python que se ejecuta como una aplicación web.

### Librerías Principales
- 🐼 **Pandas** y **NumPy** - Manipulación, limpieza, tipado y agregación de datos.
- 📊 **Plotly** (`graph_objects` y `subplots`) - Gráficos interactivos avanzados y visualizaciones estadísticas.

### Fuente de Datos
- 📄 **dld_sales_transactions.parquet:** Dataset de transacciones de venta inmobiliaria de Dubái (Dubai Land Department), almacenado en formato Parquet para una carga y lectura altamente eficiente.

### Gestor de Entorno y Despliegue
- 📦 **UV** - Gestor de paquetes y entornos de Python de alta velocidad.
- ☁️ **molab** - Plataforma de despliegue nativa para notebooks de marimo.

---

## ⚙️ Configuración del Entorno

### Prerequisitos
1. Tener instalado **Python** (la versión específica está definida en el archivo `.python-version`).
2. Tener instalado el gestor de paquetes `uv`.

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/Gbarrantes25/RealStateDubai-Dashboard.git
cd RealStateDubai-Dashboard
```

### Paso 2: Instalar Dependencias
Sincroniza el entorno virtual e instala las dependencias especificadas en pyproject.toml:

```bash
uv sync
```

### Paso 3: Ejecutar el Proyecto
Puedes ejecutar el proyecto de dos maneras:
Como aplicación web interactiva (Modo Producción):

```bash
marimo run app.py
```

Como notebook editable (Modo Desarrollo):

```bash
marimo edit app.py
```

El proyecto se abrirá automáticamente en tu navegador predeterminado (generalmente en http://localhost:2718).

## 📂 Estructura del Repositorio

```
.
├── app.py                           # Notebook marimo con el análisis y las visualizaciones
├── dld_sales_transactions.parquet   # Dataset de transacciones de venta inmobiliaria
├── pyproject.toml                   # Gestor y configuración de dependencias del proyecto
├── uv.lock                          # Archivo de lock del gestor de paquetes uv
├── .python-version                  # Especificación de la versión de Python a utilizar
├── .gitignore                       # Archivo de configuración Git
└── README.md                        # Este archivo de documentación
```

## 🔎 Algunos Hallazgos
El análisis de los datos revela tendencias clave del mercado inmobiliario de Dubái:
- 🏠 Dominio Residencial: El uso Residencial supera ampliamente en volumen de ventas a las demás categorías de uso autorizado.
- 📈 Plusvalía por Tipo: Las propiedades tipo Villa y Building muestran un crecimiento acelerado del precio por m² en los últimos 5 años, mientras que Land (terrenos) y Unit (unidades) se mantienen más estables.
- 🎯 Concentración de Mercado: Solo cerca del 14% de las áreas concentra el 80% de las ventas totales (Principio de Pareto).
- 🏙️ Expansión Premium: El número de áreas que superan la media del precio por m² pasó de 37 en 2022 a 64 en 2026, indicando una expansión de zonas de alto valor.
- 🚀 Crecimiento Extremo: Las 15 áreas con mayor crecimiento han al menos triplicado su precio por m² en un periodo de 5 años.

## 🖼️ Vistas Previas del Proyecto
<details>
  <summary>📸 Ver Capturas de Pantalla</summary>

  <img width="1390" height="575" alt="image" src="https://github.com/user-attachments/assets/f166450b-66af-4c6b-89dd-12c82ae38748" />
  <img width="1367" height="940" alt="image" src="https://github.com/user-attachments/assets/2d468ba8-5f86-4d77-a1b0-cb7f544f0ff4" />
  <img width="1396" height="727" alt="image" src="https://github.com/user-attachments/assets/402e06f2-0a7d-4cbf-863a-3f1bf4efd1e6" />
</details>

<details>
<summary>🎥 Ver Video Demostrativo</summary>

   
   Ver en YouTube: https://youtu.be/CC970ZuwjzI?si=0AzUZR8hideqjRaM
</details>

## 👤 Autor
Giancarlo Barrantes

Business Intelligence Developer | Power BI Specialist


<a href="https://www.linkedin.com/in/gb25"><img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/e0d69586-c6f9-4f66-9a3d-bc8dfa146463" /></a>
<a href="https://www.instagram.com/gbarrantes25"><img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/68773029-5e0f-49da-92e9-fb93a223dd09" />
</a>
<a href="https://www.tiktok.com/@gbarrantes25"><img width="65" height="20" alt="image" src="https://github.com/user-attachments/assets/349c87c0-1f3a-4368-8517-64a6012565c0" /></a>
<a href="https://www.youtube.com/@gbarrantes25"><img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/d9e2cb69-29ec-47fc-93ae-30896a7b533d" />
</a>

## 📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo <a href="https://mit-license.org/">LICENSE</a> para más detalles.

## ⭐ Agradecimientos
Si este proyecto te resultó útil, considera darle una ⭐ en GitHub y compartirlo con otros profesionales de Business Intelligence.

<div align="center">
   Hecho por <a href="https://gbarrantes25.github.io/">Giancarlo Barrantes</a>
</div>
