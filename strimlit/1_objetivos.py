import streamlit as st

st.set_page_config(
    page_title="objetivos del estudio",
    layout="wide"
)

st.title("objetivos del estudio")
st.markdown("---")

st.header("objetivo general")
st.write("este trabajo busca identificar los patrones de riesgo relacionados con los incidentes de tiburones en nueva caledonia. se usaran las caracteristicas de los ataques, las victimas y el entorno, como actividad, lugar y tiempo. se aplicaran metodos estadisticos simples para crear informacion que ayude a prevenir estos incidentes.")

st.markdown("---")

st.header("objetivos especificos")

st.write("""
•  se analizara cuantos ataques terminan en muerte para calcular que porcentaje de los incidentes son fatales, usando el dato is_fatal = Y en los registros.

•  se evaluara el riesgo por tipo de actividad humana. se determinara, con numeros absolutos y proporciones, que actividad concentra la mayor cantidad de ataques.

•  se delimitara la zona geografica donde ocurren los ataques. se identificaran y ordenaran las comunas con mas incidentes.

•  se describira el perfil de las victimas. se calculara la media y mediana de la edad, y se analizara la distribucion por sexo.

•  se estudiara cuando ocurren los ataques. se usaran datos agrupados por estacion del año y por hora del dia para buscar patrones de tiempo.

•  se revisara si hay relacion entre la actividad humana y la gravedad del ataque. se analizara si la proporcion de muertes varia segun la actividad y la gravedad.
""")

st.markdown("---")