import streamlit as st

st.set_page_config(
    page_title="objetivos del Estudio",
    layout="wide"
)

st.title("Objetivos del Estudio")
st.markdown("---")

st.header("Objetivo General")
st.write("Determinar los patrones descriptivos de los incidentes relacionados a ataques de tiburones registrados por todo el mundo, desde el año 1595 hasta la actualidad, mediante el uso de técnicas de estadística descriptiva, con el fin de generar información que pueda ayudar a prevenir futuros encuentros inoportunos.")

st.markdown("---")

st.header("Objetivos Especificos")

st.write("""
•  Se analizara cuantos ataques terminan en muerte para calcular que porcentaje de los incidentes son fatales, usando el dato is_fatal = Y en los registros.

•  Se evaluara el riesgo por tipo de actividad humana. se determinara, con numeros absolutos y proporciones, que actividad concentra la mayor cantidad de ataques.

•  Se delimitara la zona geografica donde ocurren los ataques. se identificaran y ordenaran las comunas con mas incidentes.

•  Se describira el perfil de las victimas. se calculara la media y mediana de la edad, y se analizara la distribucion por sexo.

•  Se estudiara cuando ocurren los ataques. se usaran datos agrupados por estacion del año y por hora del dia para buscar patrones de tiempo.

•  Se revisara si hay relacion entre la actividad humana y la gravedad del ataque. se analizara si la proporcion de muertes varia segun la actividad y la gravedad.
""")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Objetivos del Estudio")