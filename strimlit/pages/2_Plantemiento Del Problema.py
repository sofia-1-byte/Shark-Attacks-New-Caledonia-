import streamlit as st
import stilez 

st.set_page_config(
    page_title="Planteamiento del Problema - Ataques de Tiburón",
    page_icon="🦈",
    layout="wide"
)

stilez.aplicar_estilos_globales()

# titulo principal
st.title("Planteamiento del Problema")
st.markdown("---")

# contenido principal
st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
Un ataque de tiburón es un incidente en el que un tiburón muerde o ataca a un humano en su entorno natural. A pesar de la percepción popular, estos ataques son extremadamente raros y, en su mayoría, no son depredaciones intencionadas, sino que ocurren por confusión, curiosidad o defensa. Aunque los tiburones son temidos, los ataques fatales son poco frecuentes en comparación con otros incidentes marinos.

Es por esto que en este trabajo de investigación se buscará determinar los patrones descriptivos de riesgo asociados a los incidentes de tiburones registrados a nivel global. Esto se logrará mediante el uso de datos obtenidos de los ataques registrados, como la ubicación, especie de tiburón involucrada, temporada del año, fecha y hora, entre otros valores.


</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Planteamiento del Problema")