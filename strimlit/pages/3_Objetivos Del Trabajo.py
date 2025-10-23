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
st.write("Determinar los patrones descriptivos de los incidentes relacionados a ataques de tiburones registrados por todo el mundo, desde el año 1900 hasta la actualidad, mediante el uso de técnicas de estadística descriptiva, con el fin de generar información que pueda ayudar a prevenir futuros encuentros inoportunos.")

st.markdown("---")

st.header("Objetivos Especificos")

st.write("""
•  Se analizara cuantos ataques terminan en muerte para calcular que porcentaje de los incidentes son fatales.

•  Se evaluara el riesgo por tipo de actividad humana, este se determinara, con numeros absolutos y proporciones porcentuales , que actividad concentra la mayor cantidad de ataques.

•  Se delimitara la zona geografica donde ocurren los ataques, identificando y ordenando los paices con mas incidentes.

•  Se describira el perfil de las victimas, calculando la media y mediana de la edad, y se analizara la distribucion por fatalidad.

•  Se estudiara cuando ocurren los ataques, usando datos agrupados por estacion del año para buscar patrones de tiempo.

•  Se revisara si hay relacion entre la actividad realisada al momento del ataque y la gravedad del ataque, nalizando si el porcentaje de muertes varia segun la actividad y la gravedad.
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Objetivos del Estudio")