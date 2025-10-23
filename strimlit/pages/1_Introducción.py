import streamlit as st
import utils

st.set_page_config(
    page_title="Introducción - Ataques de Tiburón",
    page_icon="🦈",
    layout="wide"
)

# titulo principal
st.title("Introducción")
st.markdown("---")

# contenido principal
st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
Los ataques de tiburón han sido objeto de fascinación y temor a lo largo de la historia. Comprender las circunstancias, patrones y tendencias de estos incidentes es fundamental para promover la seguridad en las playas y la conservación de estas especies.

A nivel global, los incidentes con tiburones son extremadamente infrecuentes, especialmente si se comparan con otras causas de muerte o lesión en entornos acuáticos. No obstante, cuando ocurren, su impacto mediático y psicológico es considerable, lo que ha llevado a una creciente necesidad de comprender las circunstancias que los rodean. Factores como la localización geográfica, la actividad humana desarrollada en el momento del incidente, la especie de tiburón involucrada, la estacionalidad y las características de las víctimas son elementos clave para identificar patrones y tendencias.


Es por estos motivos que en este análisis descriptivo, exploraremos datos históricos sobre ataques de tiburón, identificando factores clave y proporcionando una visión general de su impacto global.


</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Introducción")