import streamlit as st
import utils
import stilez 

st.set_page_config(
    page_title="Analisis Descriptivo de Ataques de Tiburon - Grupo 3",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# mostrar logos
utils.mostrar_logos()

stilez.aplicar_estilos_globales()

st.title("Aplicación Principal")
st.markdown("---")

# descripcion de la aplicacion
st.markdown("""           

## Bienvenido al Análisis de Ataques de Tiburón

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
            

### Autores: Sofía Rodríguez, Roman Marcano, Diego Aguilar y Andres Mendez.            
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Aplicación Principal")