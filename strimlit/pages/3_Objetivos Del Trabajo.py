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
• **Analizar la letalidad de los ataques** para establecer la proporción porcentual exacta de incidentes clasificados como fatales (is_fatal = Y) dentro del total de registros.

• **Evaluar el riesgo por actividad** para identificar, mediante la frecuencia absoluta y relativa, la actividad humana (activity) que concentra el mayor número de ataques.

• **Delimitar la concentración geográfica de los incidentes** para visualizar y rankear los países (country) que registran la más alta frecuencia de ataques.

• **Analizar el perfil de la víctima** mediante el cálculo de la media y la mediana de la edad y la distribución de frecuencias.

• **Establecer la distribución temporal de los ataques** a través del análisis de frecuencias agrupadas por estación (season), buscando patrones de ocurrencia.

• **Examinar la relación entre variables y fatalidad** para analizar cómo la actividad, país, edad y estación se asocian con la letalidad de los incidentes mediante tablas de contingencia.
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Objetivos del Estudio")