import streamlit as st
import utils
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import os

st.set_page_config(
    page_title="grupo 2 - ataques de tiburon",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# logos 
LOGO_IMAGE1 = "logos-Ucv.png"  
LOGO_IMAGE2 = "logos-EECA.png" 

# funcion para cargar y codificar imagenes base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

# header con logos
logo1_base64 = get_base64_image(LOGO_IMAGE1)
logo2_base64 = get_base64_image(LOGO_IMAGE2)

st.markdown(
    f"""
    <div style="background-color:#4991f5;padding:10px;display:flex;justify-content:space-between;align-items:center;margin-top:-30px;">
        <img src="data:image/png;base64,{logo1_base64}" style="height:40px;margin:30px;">
        <img src="data:image/png;base64,{logo2_base64}" style="height:40px;margin:30px;">
    </div>
    """,
    unsafe_allow_html=True
)

# estilos css personalizados
st.markdown(
    """
    <style>
    :root {
        --primary-color: #4991f5;
    }
    body {
        color: #0a0a0a;
        background-color: #f5f5f5;
        font-family: 'Calibri', sans-serif;
    }
    .block-container {
        border-left: 1px solid var(--primary-color);
        border-right: 1px solid var(--primary-color);
        border-top: 1px solid var(--primary-color);
    }
    .main-title {
        color: #4991f5;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #4991f5;
        border-bottom: 2px solid #7ca0fb;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# titulo principal
st.markdown('<h1 class="main-title">analisis de patrones de ataques de tiburones en nueva caledonia</h1>', unsafe_allow_html=True)

# introduccion
st.markdown("""
### introduccion

""", unsafe_allow_html=True)

# carga de datos
@st.cache_data
def cargar_datos():
    return utils.load_and_clean_data()

with st.spinner("cargando datos..."):
    df = cargar_datos()

if df.empty:
    st.error("no se pudieron cargar los datos. verifique la conexion a la base de datos.")
    st.stop()

# metricas principales
estadisticas = utils.obtener_estadisticas_completas(df)
metricas = estadisticas['metricas_basicas']

st.markdown("---")
st.markdown('<h2 class="section-header">metricas principales</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("total registros", metricas['total_registros'])
with col2:
    st.metric("ataques fatales", metricas['ataques_fatales'])
with col3:
    st.metric("ataques no fatales", metricas['ataques_no_fatales'])
with col4:
    st.metric("tasa de fatalidad", f"{metricas['tasa_fatalidad']:.1f}%")

# objetivos del proyecto
st.markdown("---")
st.markdown('<h2 class="section-header">objetivos del estudio</h2>', unsafe_allow_html=True)

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
    objetivos = [
        "analizar cuantos ataques terminan en muerte para calcular que porcentaje de los incidentes son fatales",
        "evaluar el riesgo por tipo de actividad humana y determinar que actividad concentra mas ataques",
        "delimitar la zona geografica donde ocurren los ataques e identificar las areas con mas incidentes",
        "describir el perfil de las victimas calculando media y mediana de edad y distribucion por sexo",
        "estudiar cuando ocurren los ataques usando datos por estacion del año y hora del dia",
        "revisar si hay relacion entre la actividad humana y la gravedad del ataque"
    ]
    
    for i, objetivo in enumerate(objetivos, 1):
        st.write(f"{i}. {objetivo}")

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