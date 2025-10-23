import streamlit as st
import utils

st.set_page_config(
    page_title="Analisis Descriptivo de Ataques de Tiburon - Grupo 3",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# mostrar header con logos - SIN PARAMETROS
utils.mostrar_header()

# titulo principal
st.title("Análisis Descriptivo de Ataques de Tiburón")
st.markdown("---")

# descripcion de la aplicacion
st.markdown("""
### Bienvenido al análisis de ataques de tiburón

Esta aplicación permite explorar y analizar los patrones de ataques de tiburones a nivel mundial 
desde el año 1595 hasta la actualidad. Utiliza técnicas de estadística descriptiva y consultas 
SQL para identificar factores de riesgo y características de los incidentes.

### Datos del estudio

El análisis se basa en el dataset global de ataques de tiburón, que contiene información sobre:
- Ubicación geográfica de los incidentes
- Especie de tiburón involucrada
- Actividad de la víctima al momento del ataque
- Fecha, hora y estación del año
- Gravedad del incidente (fatal/no fatal)
- Características demográficas de las víctimas
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Aplicación Principal")