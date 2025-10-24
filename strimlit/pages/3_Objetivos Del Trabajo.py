import streamlit as st
import stilez 

st.set_page_config(
    page_title="objetivos del Estudio",
    page_icon="🦈",
    layout="wide"
)

stilez.aplicar_estilos_globales()

# titulo principal
st.title("Objetivos del Estudio")
st.markdown("---")

# contenido principal
st.header("Objetivo General")
st.write("Identificar y analizar los patrones descriptivos de los incidentes de ataques de tiburones a nivel mundial mediante las estadísticas descriptiva, con el fin de comprender los factores asociados a estos eventos y contribuir a la prevención de encuentros futuros.")

st.markdown("---")

st.header("Objetivos Especificos")

st.write("""
• **Analizar las actividades humanas** para identificar las más riesgosas y su relación con la fatalidad.

• **Examinar los países** para ubicar los de mayor incidencia y su distribución de casos fatales.

• **Evaluar las estaciones del año** para determinar las más peligrosas y su asociación con la fatalidad.

• **Analizar la edad de las víctimas** para describir los grupos más afectados y su relación con la fatalidad.

• **Investigar la tasa global de fatalidad** para establecer la proporción de ataques mortales.

• **Analizar la relación entre actividad y fatalidad** para determinar las actividades con mayor letalidad.

• **Examinar la distribución por grupos de edad** para identificar patrones de vulnerabilidad según la fatalidad.

• **Evaluar las variaciones estacionales** para detectar cambios en la gravedad de los ataques.
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Objetivos del Estudio")