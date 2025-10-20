import streamlit as st
import utils
import pandas as pd

st.set_page_config(
    page_title="Analisis de Datos",
    layout="wide"
)

st.title("Analisis Descriptivo de Datos")
st.markdown("---")

# Cargar datos 
df, estadisticas = utils.cargar_datos_y_estadisticas()

if df.empty:
    st.error("no se pudieron cargar los datos.")
    st.stop()

metricas = estadisticas['metricas_basicas']

st.header("Tablas de Fatalidad")

tabla_fatalidad = utils.analizar_frecuencias(df, 'is_fatal_cat', excluir_desconocido=True)

if not tabla_fatalidad.empty:
    st.dataframe(tabla_fatalidad, use_container_width=True)
    
    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    ## Interpretación 
    
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("estadisticas descriptivas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tasa de Fatalidad", f"{metricas['tasa_fatalidad']:.1f}%", 
                 help=f"{metricas['ataques_fatales']} casos fatales")
    with col2:
        st.metric("Tasa de no Fatalidad", f"{100 - metricas['tasa_fatalidad']:.1f}%", 
                 help=f"{metricas['ataques_no_fatales']} casos no fatales")

st.markdown("---")

st.header("Tabla de Actividades")

tabla_actividades = utils.analizar_frecuencias(df, 'activity', excluir_desconocido=True)

if not tabla_actividades.empty:
    st.dataframe(tabla_actividades, use_container_width=True)
    
    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    ## Interpretación 
    
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Estadisticas Descriptivas")
    st.write("5 actividades mas atacadas:")
    
    for i, (_, row) in enumerate(tabla_actividades.head(5).iterrows(), 1):
        st.write(f"{i}. {row['Categoria']}: {row['Frecuencia Absoluta']} incidentes ({row['Frecuencia Relativa %']}%)")

st.markdown("---")

st.header("Tabla de Paises")

tabla_paises = utils.analizar_frecuencias(df, 'country', excluir_desconocido=True)

if not tabla_paises.empty:
    st.dataframe(tabla_paises, use_container_width=True)

    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    ## Interpretación 
    
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Estadisticas Descriptivas")
    st.write("Top 5 Paises Mas Atacados:")
    
    for i, (_, row) in enumerate(tabla_paises.head(5).iterrows(), 1):
        st.write(f"{i}. {row['Categoria']}: {row['Frecuencia Absoluta']} incidentes ({row['Frecuencia Relativa %']}%)")

st.markdown("---")

st.header("Tablas de Victimas")

df_edad_grupos = df.copy()
bins = [0, 18, 30, 45, 60, 100]
labels = ['0-18', '19-30', '31-45', '46-60', '60+']
df_edad_grupos['grupo_edad'] = pd.cut(df_edad_grupos['age'], bins=bins, labels=labels, right=False)

tablas_edad = utils.crear_tablas_doble_entrada(df_edad_grupos, 'grupo_edad', 'is_fatal_cat')

if tablas_edad:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Frecuencias Absolutas", "Porcentaje del Total", 
        "Porcentaje por Fila", "Porcentaje por Columna"
    ])
    
    with tab1:
        st.dataframe(tablas_edad['absoluta'], use_container_width=True)
    with tab2:
        st.dataframe(tablas_edad['porcentaje_total'], use_container_width=True)
    with tab3:
        st.dataframe(tablas_edad['condicional_filas'], use_container_width=True)
    with tab4:
        st.dataframe(tablas_edad['condicional_columnas'], use_container_width=True)

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>

## Interpretación 

</div>
""", unsafe_allow_html=True)

st.subheader("Estadisticas Descriptivas de la Edad")

if not estadisticas['estadisticas_edad'].empty:
    st.dataframe(estadisticas['estadisticas_edad'], use_container_width=True)

st.markdown("---")

st.header("Tabla de Estaciones")

tabla_estaciones = utils.analizar_frecuencias(df, 'season', excluir_desconocido=True)

if not tabla_estaciones.empty:
    st.dataframe(tabla_estaciones, use_container_width=True)
    
    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    ## Interpretación
    
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Estadisticas Descriptivas")
    st.write("Top Estaciones con Mas Ataques:")
    
    for i, (_, row) in enumerate(tabla_estaciones.iterrows(), 1):
        st.write(f"{i}. {row['Categoria']}: {row['Frecuencia Absoluta']} incidentes ({row['Frecuencia Relativa %']}%)")

st.markdown("---")

st.header("Tabla de Actividad vs Fatalidad")

tablas_actividad = utils.crear_tablas_doble_entrada(df, 'activity', 'is_fatal_cat')

if tablas_actividad:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Frecuencias Absolutas", "Porcentaje del Total", 
        "Porcentaje por Fila", "Porcentaje por Columna"
    ])
    
    with tab1:
        st.dataframe(tablas_actividad['absoluta'], use_container_width=True)
    with tab2:
        st.dataframe(tablas_actividad['porcentaje_total'], use_container_width=True)
    with tab3:
        st.dataframe(tablas_actividad['condicional_filas'], use_container_width=True)
    with tab4:
        st.dataframe(tablas_actividad['condicional_columnas'], use_container_width=True)

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>

## Interpretación 

</div>
""", unsafe_allow_html=True)

st.subheader("Estadisticas Descriptivas")

if not estadisticas['tasas_actividad'].empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("5 Actividades Mas Fatales:")
        for i, (actividad, row) in enumerate(estadisticas['tasas_actividad'].head(5).iterrows(), 1):
            st.write(f"{i}. {actividad}: {row['Tasa Fatalidad %']}%")
    
    with col2:
        st.write("5 Actividades Menos Fatales:")
        actividades_significativas = estadisticas['tasas_actividad'][estadisticas['tasas_actividad']['Total'] >= 5]
        for i, (actividad, row) in enumerate(actividades_significativas.tail(5).iterrows(), 1):
            st.write(f"{i}. {actividad}: {row['Tasa Fatalidad %']}%")

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Estadísticas Descriptivas")
