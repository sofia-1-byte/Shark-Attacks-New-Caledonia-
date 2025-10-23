import streamlit as st
import utils
import pandas as pd

st.set_page_config(
    page_title="Análisis de Datos",
    page_icon="🦈",
    layout="wide"
)

# titulo principal
st.title("Análisis Descriptivo de Datos")
st.markdown("---")

# Cargar datos 
df, estadisticas = utils.cargar_datos_y_estadisticas()

metricas = estadisticas['metricas_basicas']

st.header("Analisis de Fatalidad")

st.subheader("Tabla de Fatalidad")

tabla_fatalidad = utils.analizar_frecuencias(df, 'is_fatal_cat', excluir_desconocido=True)

if not tabla_fatalidad.empty:
    st.dataframe(tabla_fatalidad, use_container_width=True)
    
    st.subheader("Estadísticas descriptivas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Porcentaje de Fatalidad", f"{metricas['tasa_fatalidad']:.1f}%", 
                 help=f"{metricas['ataques_fatales']} casos fatales")
    with col2:
        st.metric("Porcentaje de no Fatalidad", f"{100 - metricas['tasa_fatalidad']:.1f}%", 
                 help=f"{metricas['ataques_no_fatales']} casos no fatales")

st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    Se puede observar que de un total de 5001 ataques registrados, 3902 ataques son ataques no fatales, representando un 78% del total. Mientras que solo 1099 ataques son registrados como fatales, siendo un 22% del total. Esto indica que los ataques de tiburones poseen una baja tasa de fatalidad.
                
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("Analisis de Actividades Atacadas")

st.subheader("Tabla de Actividades Atacadas")

tabla_actividades = utils.analizar_frecuencias(df, 'activity', excluir_desconocido=True)

if not tabla_actividades.empty:
    st.dataframe(tabla_actividades, use_container_width=True)
    

    
    st.subheader("Top de las 5 Actividades Más Atacadas")
    
    for i, (_, row) in enumerate(tabla_actividades.head(5).iterrows(), 1):
        st.write(f"{i}. {row['Categoria']}: {row['Frecuencia Absoluta']} incidentes ({row['Frecuencia Relativa %']}%)")


    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    Las actividades más realizadas antes de sufrir un ataque de tiburón son: surfear, con 1069 incidentes; bodyboarding, con 976 incidentes y pescar, con 864 incidentes.

    Por otra parte, las actividades menos comunes al sufrir un ataque de tiburón son: flotar en el agua, con 14 incidentes; remar, con 13 incidentes y el suceso que menos ocurre durante ataques de tiburones es caerse de la borda de una embarcación, con solo 4 ataques registrados.

    Podemos decir que la mayoría de ataques se producen al realizar actividades que requieran estar mucho tiempo en el agua y que hacen que el tiburón confunde a la persona con una presa. En el caso de la pesca se puede deber a la atracción del tiburón buscando alguna presa.

    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("Analisis de Países Atacados")

st.subheader("Tabla de Países Atacados")

tabla_paises = utils.analizar_frecuencias(df, 'country', excluir_desconocido=True)

if not tabla_paises.empty:
    st.dataframe(tabla_paises, use_container_width=True)

    st.subheader("Top 5 Países Más Atacados")
    
    for i, (_, row) in enumerate(tabla_paises.head(5).iterrows(), 1):
        st.write(f"{i}. {row['Categoria']}: {row['Frecuencia Absoluta']} incidentes ({row['Frecuencia Relativa %']}%)")

    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    Los 3 países con más ataques registrados son con diferencia Estados Unidos, Australia y Sudáfrica. Esto se debe a diversos factores como: alta densidad de población en locaciones costeras;  la gran costa marítima que poseen, ideales para todo tipo de actividades acuáticas; y por último, las especies de tiburones con más ataques habitan en estos países.

    En cambio, los países con menos ataques registrados suelen tener climas no favorables para la mayoría de especies de tiburones causantes de ataques, además de tener un bajo número de población tanto en el territorio total como en las costas. La mayoría de países que se encuentran en esta situación poseen climas fríos como Islandia o las islas Británicas, no poseen grandes líneas costeras como Líbano o países de la península de los Balcanes, o simplemente son países que no poseen gran actividad en los océanos.

    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("Analisis de Victimas vs Fatalidad")

st.subheader("Tabla de Victimas vs Fatalidad")

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


st.subheader("Estadísticas Descriptivas de la Edad")

if not estadisticas['estadisticas_edad'].empty:
    st.dataframe(estadisticas['estadisticas_edad'], use_container_width=True)

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>

 La gran mayoría de víctimas de estos encuentros inoportunos poseen una edad en el rango de entre 19 a 30 años, con un total de 3084 ataques de tiburón a este grupo, siendo con diferencia el grupo de edad más afectado con un porcentaje del 61.67%. 
 Los demás grupos de edad afectados en orden son: entre 18 a 20 años con 816 afectados (un 16,32%), entre 31 a 45 años con 690 afectados (13,8%), entre 46 a 60 años con 316 afectados (6,32%), y el grupo menos afectado son las personas mayores a 60 años con solo 95 victimas (1,9%).

 La media de edad de las víctimas es de 26,59 años, con una desviación de 11,02 años con respecto a la media.


</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.header("Analisis de Estaciones en las que Hubo Ataques")

st.subheader("Tabla de Estaciones en las que Hubo Ataques")

tabla_estaciones = utils.analizar_frecuencias(df, 'season', excluir_desconocido=True)

if not tabla_estaciones.empty:
    st.dataframe(tabla_estaciones, use_container_width=True)
    
    st.subheader("Top Estaciones con Mas Ataques")
    
    for i, (_, row) in enumerate(tabla_estaciones.iterrows(), 1):
        st.write(f"{i}. {row['Categoria']}: {row['Frecuencia Absoluta']} incidentes ({row['Frecuencia Relativa %']}%)")

    st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    La estación del año con más ataques de tiburón registrados es el invierno. Esto puede deberse a que durante esa época la noche suele ser más duradera, cuando los tiburones son mucho más activos, además que en ciertos lugares del hemisferio sur, como lo es Australia, su verano ocurre de diciembre a marzo, donde en otros lugares sería invierno, haciendo que mucha más población se encuentre en las playas, aumentando la posibilidad de algún ataque.

    Después del invierno, las estaciones con más ataques registrados son otoño y verano, siendo primavera la estación con menos ataques registrados.
    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("Analisis de Actividad vs Fatalidad")

st.subheader("Tabla de Actividad vs Fatalidad")

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

st.subheader("Top Actividades Más y Menos Fatales")

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


st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>

 Se puede apreciar que la actividad con mayor tasa de mortalidad con bastante diferencia es caerse de la borda de una embarcación, con una tasa de mortalidad del 75%. Seguido de este, las otras dos actividades más fatales son: bañarse (42,42% de mortalidad) y nadar (37,5%).

 Por su parte, las actividades menos fatales son boogie boarding (4,76% de mortalidad), remar y surfskiing, con un 0% de mortalidad.


</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Estadísticas Descriptivas")