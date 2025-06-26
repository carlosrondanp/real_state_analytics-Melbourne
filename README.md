# Proyecto de Valuación Inmobiliaria en Melbourne 🏘️📍

Este repositorio contiene un flujo completo para la estimación del valor de propiedades en Melbourne, Australia. Se utilizó un enfoque integral que combina diversas fuentes de datos, procesamiento geoespacial y modelos de machine learning avanzados.

## 🔍 Fuentes de Datos

- **Kaggle - Melbourne Housing Market**: Dataset base con información detallada de propiedades.
- **OpenStreetMap (OSM)**: Utilizado para extraer lugares cercanos (colegios, hospitales, estaciones, etc.) mediante `osmnx` para enriquecer las variables.
- **Web Scraping (Google Maps)**: Empleado para obtener coordenadas geográficas (latitud, longitud) de propiedades con información incompleta.

## ⚙️ Estructura del Proyecto

| Archivo | Descripción |
|--------|-------------|
| `1.conexiones.ipynb` | Configuración de librerías y conexión a servicios externos. |
| `1.get_osm_places.ipynb` | Extracción y agrupación de lugares relevantes desde OpenStreetMap. |
| `1.scraping_geo.ipynb` | Scraping de coordenadas geográficas usando direcciones del dataset. |
| `2.preprocessing.ipynb` | Limpieza y procesamiento multivariante + geoespacial. |
| `3.distances_to_predio.ipynb` | Cálculo de distancias entre propiedades y puntos de interés. |
| `main.ipynb` | Entrenamiento del modelo final con LightGBM y Optuna. |

## 🧪 Procesamiento y Modelamiento

- **Imputación de coordenadas** mediante scraping basado en dirección.
- **Generación de nuevas variables** como distancias a lugares clave (educación, salud, transporte).
- **Limpieza multivariada** con eliminación de outliers y validación geoespacial.
- **Modelado** con LightGBM ajustado con Optuna para minimizar el error cuadrático medio (RMSE).
- **Evaluación** usando validación cruzada.

## 🛠️ Librerías clave

- `pandas`, `numpy`, `geopandas`, `shapely`, `matplotlib`
- `osmnx`, `folium`, `scikit-learn`, `lightgbm`, `optuna`
- `selenium` y `requests` para scraping

## 📈 Objetivo

Mejorar la precisión de predicción del precio de propiedades integrando características del entorno y completando datos faltantes con fuentes externas. El enfoque está orientado a la aplicabilidad en contextos reales de valoración inmobiliaria.

---

Autor: Carlos Rondan