import pandas as pd
import plotly.express as px
import streamlit as st
import utils
import utilsg
import stilez 

st.set_page_config(
    page_title="Gráficos e Interpretación de los Datos 📊",
    page_icon="🦈",
    layout="wide")

stilez.aplicar_estilos_globales()

# título principal
st.title("Análisis Visual de Ataques de Tiburón 📊")
st.markdown("---")

# Cargar datos
df = utilsg.load_and_clean_data1()

# 1. FATALIDAD (siempre gráfico circular)
st.header("1. Análisis de Fatalidad 💀")

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(utilsg.grafico_fatalidad_interactivo(), use_container_width=True)

with col2:
    st.markdown("""
    **Interpretación:**
    - **78%** de los ataques son **no fatales**
    - **22%** resultan en fatalidades
    - La mayoría de víctimas sobreviven al encuentro
    - Los ataques fatales son la excepción, no la regla
    """)

st.markdown("---")

# 2. ACTIVIDADES
st.header("2. Análisis de Actividades 🌊")

col1, col2 = st.columns([3, 1])
with col2:
    cond_act = st.checkbox("Condicionar por Fatalidad", key="actividad")

with col1:
    fig_act = utilsg.grafico_actividad_interactivo(condicionar_fatalidad=cond_act)
    st.plotly_chart(fig_act, use_container_width=True)

# Interpretación condicional
if cond_act:
    st.markdown("""
    **Interpretación - Condicionado por Fatalidad:**
    - La **natación** presenta la **mayor tasa de fatalidad** 
    - **Bodyboarding** y **pesca** siguen en riesgo con tasas significativas
    - Actividades como **surfing** tienen menor tasa de fatalidad relativa
    """)
else:
    st.markdown("""
    **Interpretación:**
    - **Surfing**, **Bodyboarding**, y **Pesca** son las actividades más atacadas
    - Distribución refleja popularidad de actividades en zonas costeras
    """)

st.markdown("---")

# 3. EDAD - Distribución
st.header("3. Análisis Demográfico - Distribución de Edad 👥")

col1, col2 = st.columns([3, 1])
with col2:
    cond_edad = st.checkbox("Condicionar por Fatalidad", key="edad")

with col1:
    fig_edad = utilsg.grafico_edad_interactivo(condicionar_fatalidad=cond_edad)
    st.plotly_chart(fig_edad, use_container_width=True)

# Interpretación condicional
if cond_edad:
    st.markdown("""
    **Interpretación - Condicionado por Fatalidad:**
    - Distribución similar entre fatal y no fatal, con ligero sesgo
    - **Adultos jóvenes** (20-35 años) predominan en ambos grupos
    - Mayores de 60 años muestran proporción similar de fatalidad
    - No hay grupo etario con riesgo desproporcionadamente alto
    - La edad no parece ser un factor determinante en la fatalidad
    """)
else:
    st.markdown("""
    **Interpretación:**
    - Distribución **leptocúrtica** con sesgo positivo
    - **Media de edad**: 32.06 años
    - **Pico principal**: 20-24 años (adultos jóvenes)
    - **Jóvenes y adultos jóvenes** son los más afectados
    - Refleja perfil demográfico de actividades de riesgo
    - Menor participación de niños y adultos mayores
    """)

st.markdown("---")

# 4. EDAD - Grupos
st.header("4. Análisis Demográfico - Grupos de Edad 👥")

col1, col2 = st.columns([3, 1])
with col2:
    cond_grupo_edad = st.checkbox("Condicionar por Fatalidad", key="grupo_edad")

with col1:
    fig_grupo_edad = utilsg.grafico_grupo_edad_interactivo(condicionar_fatalidad=cond_grupo_edad)
    st.plotly_chart(fig_grupo_edad, use_container_width=True)

# Interpretación condicional
if cond_grupo_edad:
    st.markdown("""
    **Interpretación - Condicionado por Fatalidad:**
    - **19-30 años**: Mayor número absoluto de fatalidades 
    - **0-18 años**: Tasa de fatalidad moderada 
    - **31-45 años**: Segunda en fatalidades absolutas 
    - Distribución proporcional a la frecuencia por grupo
    - No hay grupo de edad con riesgo significativamente mayor
    - Factores como condición física pueden influir en la supervivencia
    """)
else:
    st.markdown("""
    **Interpretación:**
    - **19-30 años** (grupo más afectado)
    - **0-18 años** (segundo lugar)
    - **31-45 años** (tercer lugar)
    - **46-60 años** (cuarto lugar)
    - **60+ años** (menos afectado)
    - **Adultos jóvenes** predominan claramente
    - Refleja perfil de actividades recreativas acuáticas
    """)

st.markdown("---")

# 5. TEMPORADAS
st.header("5. Análisis Estacional 📅")

col1, col2 = st.columns([3, 1])
with col2:
    cond_temp = st.checkbox("Condicionar por Fatalidad", key="temporada")

with col1:
    fig_temp = utilsg.grafico_temporada_interactivo(condicionar_fatalidad=cond_temp)
    st.plotly_chart(fig_temp, use_container_width=True)

# Interpretación condicional
if cond_temp:
    st.markdown("""
    **Interpretación - Condicionado por Fatalidad:**
    - **Verano**: Mayor proporción de fatalidades 
    - **Invierno**: Mayor número de ataques pero menor tasa fatal
    - **Otoño** y **Primavera**: Tasas intermedias de fatalidad
    - Posible relación con especies migratorias y turismo
    - En verano, mayor presencia de bañistas ocasionales
    - En invierno, predominio de surfistas y deportistas experimentados
    """)
else:
    st.markdown("""
    **Interpretación:**
    - **Invierno** (más ataques)
    - **Otoño** (segundo lugar)
    - **Verano** (tercer lugar)  
    - **Primavera**  (menos ataques)
    - Diferencias menores entre estaciones 
    """)

st.markdown("---")
st.caption("Dashboard de Análisis de Ataques de Tiburón | Graficos")
