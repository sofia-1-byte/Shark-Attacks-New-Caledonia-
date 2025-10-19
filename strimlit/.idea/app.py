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
st.title("Analisis Descriptivo de Ataques de Tiburon")
st.markdown("---")

# descripcion de la aplicacion
st.markdown("""
### bienvenido al analisis de ataques de tiburon

esta aplicacion permite explorar y analizar los patrones de ataques de tiburones a nivel mundial 
desde el año 1595 hasta la actualidad. utiliza tecnicas de estadistica descriptiva y consultas 
sql para identificar factores de riesgo y caracteristicas de los incidentes.

### datos del estudio

el analisis se basa en el dataset global de ataques de tiburon, que contiene informacion sobre:
- ubicacion geografica de los incidentes
- especie de tiburon involucrada
- actividad de la victima al momento del ataque
- fecha, hora y estacion del año
- gravedad del incidente (fatal/no fatal)
- caracteristicas demograficas de las victimas
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Applicación Principal")