import streamlit as st
import utils
import pandas as pd
import plotly.express as px
from PIL import Image
import os

st.set_page_config(
    page_title="grupo 2 - ataques de tiburon",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar logo UCV
def cargar_logo():
    try:
        # Intentar diferentes rutas posibles
        rutas = ["Logo-Ucv.png", "logos/Logo-Ucv.png", "./Logo-Ucv.png"]
        for ruta in rutas:
            if os.path.exists(ruta):
                return Image.open(ruta)
        return None
    except:
        return None

# Cargar logo
logo_ucv = cargar_logo()

# Header simple con solo logo UCV
col1, col2 = st.columns([1, 4])

with col1:
    if logo_ucv:
        st.image(logo_ucv, width=80)

with col2:
    st.markdown('<h1 style="color:#4991f5;margin-top:20px;">analisis descriptivo de patrones de ataques de tiburones</h1>', unsafe_allow_html=True)

st.markdown("---")

# Introduccion
st.markdown("### introduccion")
st.markdown("""
los ataques de tiburon representan un fenomeno de interes tanto para la seguridad publica como para la conservacion marina. 
en nueva caledonia, territorio con una rica biodiversidad marina, estos incidentes tienen implicaciones importantes para el turismo, 
las actividades recreativas y la percepcion publica sobre los tiburones.
""")

# Carga de datos
@st.cache_data
def cargar_datos():
    return utils.load_and_clean_data()

with st.spinner("cargando datos..."):
    df = cargar_datos()

if df.empty:
    st.error("no se pudieron cargar los datos. verifique la conexion a la base de datos.")
    st.stop()

# Metricas principales
estadisticas = utils.obtener_estadisticas_completas(df)
metricas = estadisticas['metricas_basicas']

st.markdown("---")
st.markdown("### metricas principales")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("total registros", metricas['total_registros'])
with col2:
    st.metric("ataques fatales", metricas['ataques_fatales'])
with col3:
    st.metric("ataques no fatales", metricas['ataques_no_fatales'])
with col4:
    st.metric("tasa de fatalidad", f"{metricas['tasa_fatalidad']:.1f}%")

# Objetivos
st.markdown("---")
st.markdown("### objetivos del estudio")

col_obj1, col_obj2 = st.columns(2)

with col_obj1:
    st.subheader("objetivo general")
    st.info("""
    este trabajo busca identificar los patrones de riesgo relacionados con los incidentes de tiburones 
    en nueva caledonia. se usaran las caracteristicas de los ataques, las victimas y el entorno, 
    como actividad, lugar y tiempo. se aplicaran metodos estadisticos simples para crear informacion 
    que ayude a prevenir estos incidentes.
    """)

with col_obj2:
    st.subheader("objetivos especificos")
    st.write("• analizar cuantos ataques terminan en muerte para calcular que porcentaje de los incidentes son fatales")
    st.write("• evaluar el riesgo por tipo de actividad humana y determinar que actividad concentra mas ataques")
    st.write("• delimitar la zona geografica donde ocurren los ataques e identificar las areas con mas incidentes")
    st.write("• describir el perfil de las victimas calculando media y mediana de edad y distribucion por sexo")
    st.write("• estudiar cuando ocurren los ataques usando datos por estacion del año y hora del dia")
    st.write("• revisar si hay relacion entre la actividad humana y la gravedad del ataque")



# visualizacion de datos basicos
st.markdown("---")
st.markdown('<h2 class="section-header">visualizacion de datos</h2>', unsafe_allow_html=True)

# selector de año (simulado)
option = st.selectbox('tipo de analisis:', ['actividades mas comunes', 'distribucion por pais', 'patrones temporales'])

if option == 'actividades mas comunes':
    tabla_actividades = utils.analizar_frecuencias(df, 'activity', excluir_desconocido=True)
    if not tabla_actividades.empty:
        st.dataframe(tabla_actividades.head(10), use_container_width=True)
        
        # grafica de actividades
        fig_act = px.bar(
            tabla_actividades.head(8),
            x='Categoria',
            y='Frecuencia Absoluta',
            title='actividades con mayor numero de ataques',
            color='Frecuencia Absoluta',
            color_continuous_scale='blues'
        )
        st.plotly_chart(fig_act, use_container_width=True)

elif option == 'distribucion por pais':
    tabla_paises = utils.analizar_frecuencias(df, 'country', excluir_desconocido=True)
    if not tabla_paises.empty:
        st.dataframe(tabla_paises.head(10), use_container_width=True)

elif option == 'patrones temporales':
    tabla_estaciones = utils.analizar_frecuencias(df, 'season', excluir_desconocido=True)
    if not tabla_estaciones.empty:
        st.dataframe(tabla_estaciones, use_container_width=True)

# estadisticas de edad
st.markdown("---")
st.markdown('<h2 class="section-header">estadisticas descriptivas</h2>', unsafe_allow_html=True)

if not estadisticas['estadisticas_edad'].empty:
    st.subheader("estadisticas de edad por tipo de ataque")
    st.dataframe(estadisticas['estadisticas_edad'], use_container_width=True)

# tasas de fatalidad por actividad
if not estadisticas['tasas_actividad'].empty:
    st.subheader("tasas de fatalidad por actividad")
    st.dataframe(estadisticas['tasas_actividad'].head(10), use_container_width=True)

# conclusiones
st.markdown("---")
st.markdown('<h2 class="section-header">conclusiones preliminares</h2>', unsafe_allow_html=True)

st.markdown("""

""", unsafe_allow_html=True)

# footer
st.markdown("---")
st.caption("shark attack analytics | analisis de patrones de ataques de tiburon | nueva caledonia")