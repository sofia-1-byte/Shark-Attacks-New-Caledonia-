import streamlit as st
import utils
import pandas as pd
import stilez 

st.set_page_config(
    page_title="Análisis de Datos",
    page_icon="🦈",
    layout="wide"
)

stilez.aplicar_estilos_globales()
stilez.aplicar_estilos_tablas()

# titulo principal
st.title("Análisis Descriptivo de Datos")
st.markdown("---")

# Cargar datos 
df, estadisticas = utils.cargar_datos_y_estadisticas()

metricas = estadisticas['metricas_basicas']

st.header("Análisis de Fatalidad")

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

st.header("Análisis de Actividades Atacadas")

st.subheader("Tabla de Actividades Atacadas")

# Botón para condicionar por fatalidad
condicionar_fatalidad_act = st.checkbox("Condicionar por Fatalidad", key="actividades")

if condicionar_fatalidad_act:
    # Mostrar tabla de doble entrada
    tablas_actividad_fatalidad = utils.crear_tablas_doble_entrada(df, 'activity', 'is_fatal_cat')
    
    if tablas_actividad_fatalidad:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Frecuencias Absolutas", "Porcentaje del Total", 
            "Porcentaje por Fila", "Porcentaje por Columna"
        ])
        
        with tab1:
            st.dataframe(tablas_actividad_fatalidad['absoluta'], use_container_width=True)
        with tab2:
            st.dataframe(tablas_actividad_fatalidad['porcentaje_total'], use_container_width=True)
        with tab3:
            st.dataframe(tablas_actividad_fatalidad['condicional_filas'], use_container_width=True)
        with tab4:
            st.dataframe(tablas_actividad_fatalidad['condicional_columnas'], use_container_width=True)
else:
    tabla_actividades = utils.analizar_frecuencias(df, 'activity', excluir_desconocido=True)
    if not tabla_actividades.empty:
        st.dataframe(tabla_actividades, use_container_width=True)

st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    Las actividades más realizadas antes de sufrir un ataque de tiburón son: surfear, con 1069 incidentes; bodyboarding, con 976 incidentes y pescar, con 864 incidentes.

    Por otra parte, las actividades menos comunes al sufrir un ataque de tiburón son: flotar en el agua, con 14 incidentes; remar, con 13 incidentes y el suceso que menos ocurre durante ataques de tiburones es caerse de la borda de una embarcación, con solo 4 ataques registrados.

    Si condicionamos la tabla de actividades por fatalidad podemos observar que la actividad más mortal es nadar, con 324 encuentros (6,48% de los ataques totales). A este le siguen: bodyboarding, con 313 víctimas fatales (6,26%), y pescar, con 164 fatalidades (3,28%). 

    En cambio, las actividades menos fatales son remar, surfskiing y boogie boarding, con 0, 0 y 2 ataques fatales respectivamente, representando solo el 0,04% de los ataques totales.
        
    Podemos decir que la mayoría de ataques se producen al realizar actividades que requieran estar mucho tiempo en el agua y que hacen que el tiburón confunde a la persona con una presa. En el caso de la pesca se puede deber a la atracción del tiburón buscando alguna presa.

    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("Análisis de Países Atacados")

st.subheader("Tabla de Países Atacados")

# Botón para condicionar por fatalidad
condicionar_fatalidad_paises = st.checkbox("Condicionar por Fatalidad", key="paises")

if condicionar_fatalidad_paises:
    # Mostrar tabla de doble entrada
    tablas_paises_fatalidad = utils.crear_tablas_doble_entrada(df, 'country', 'is_fatal_cat')
    
    if tablas_paises_fatalidad:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Frecuencias Absolutas", "Porcentaje del Total", 
            "Porcentaje por Fila", "Porcentaje por Columna"
        ])
        
        with tab1:
            st.dataframe(tablas_paises_fatalidad['absoluta'], use_container_width=True)
        with tab2:
            st.dataframe(tablas_paises_fatalidad['porcentaje_total'], use_container_width=True)
        with tab3:
            st.dataframe(tablas_paises_fatalidad['condicional_filas'], use_container_width=True)
        with tab4:
            st.dataframe(tablas_paises_fatalidad['condicional_columnas'], use_container_width=True)
else:
    tabla_paises = utils.analizar_frecuencias(df, 'country', excluir_desconocido=True)
    if not tabla_paises.empty:
        st.dataframe(tabla_paises, use_container_width=True)

st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    Los 3 países con más ataques registrados son con diferencia Estados Unidos, Australia y Sudáfrica. Esto se debe a diversos factores como: alta densidad de población en locaciones costeras;  la gran costa marítima que poseen, ideales para todo tipo de actividades acuáticas; y por último, las especies de tiburones con más ataques habitan en estos países.

    En cambio, los países con menos ataques registrados suelen tener climas no favorables para la mayoría de especies de tiburones causantes de ataques, además de tener un bajo número de población tanto en el territorio total como en las costas. La mayoría de países que se encuentran en esta situación poseen climas fríos como Islandia o las islas Británicas, no poseen grandes líneas costeras como Líbano o países de la península de los Balcanes, o simplemente son países que no poseen gran actividad en los océanos.

    Al condicionar esta variable con la de fatalidad, se puede apreciar que el país con mayor cantidad de ataques mortales es Australia, con 245 ataques (4,9% del total); seguido están Estados Unidos y Sudáfrica, con 188 (3,76%) y 110 (2,2%) ataques respectivamente.

            
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.header("Análisis de Edad de Víctimas")

st.subheader("Tabla de Edad de Víctimas")

# Botón para condicionar por fatalidad
condicionar_fatalidad_edad = st.checkbox("Condicionar por Fatalidad", key="edad")

df_edad_grupos = df.copy()
bins = [0, 18, 30, 45, 60, 100]
labels = ['0-18', '19-30', '31-45', '46-60', '60+']
df_edad_grupos['grupo_edad'] = pd.cut(df_edad_grupos['age'], bins=bins, labels=labels, right=False)

if condicionar_fatalidad_edad:
    # Mostrar tabla de doble entrada
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
else:
    # Mostrar tabla simple de grupos de edad
    tabla_edad_simple = utils.analizar_frecuencias(df_edad_grupos, 'grupo_edad', excluir_desconocido=True)
    if not tabla_edad_simple.empty:
        st.dataframe(tabla_edad_simple, use_container_width=True)

st.subheader("Estadísticas Descriptivas de la Edad")

if not estadisticas['estadisticas_edad'].empty:
    st.dataframe(estadisticas['estadisticas_edad'], use_container_width=True)

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>

 La mayoría de víctimas de estos encuentros inoportunos poseen una edad en el rango de entre 19 a 30 años, con un total de 1851 ataques de tiburón a este grupo, siendo con diferencia el grupo de edad más afectado con un porcentaje del 37,01%. 

 Los demás grupos de edad afectados en orden son: entre 0 a 18 años con 1026 afectados (un 20,52%), entre 31 a 45 años con 942 afectados (18,84%), entre 46 a 60 años con 669 afectados (13,38%), y el grupo menos afectado son las personas mayores a 60 años con solo 513 víctimas (10,26%).

 La media de edad de las víctimas es de 32,06 años, con una desviación de 17,33 años con respecto a la media.

 Si se condiciona esta variable con la de fatalidad, se puede visualizar que los grupos de edad con mayor cantidad de ataques fatales son: de 19 a 30 años con 424 ataques (8,48% del total de ataques), 31 a 45 años con 197 ataques (3,94%), 0 a 18 años con 186 ataques (3,72%), 46 a 60 años con 155 ataques (3,1%), y los mayores de 60 años con 137 ataques registrados como mortales (2,74%).


</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.header("Análisis de Estaciones en las que Hubo Ataques")

st.subheader("Tabla de Estaciones en las que Hubo Ataques")

# Botón para condicionar por fatalidad
condicionar_fatalidad_estaciones = st.checkbox("Condicionar por Fatalidad", key="estaciones")

if condicionar_fatalidad_estaciones:
    # Mostrar tabla de doble entrada
    tablas_estaciones_fatalidad = utils.crear_tablas_doble_entrada(df, 'season', 'is_fatal_cat')
    
    if tablas_estaciones_fatalidad:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Frecuencias Absolutas", "Porcentaje del Total", 
            "Porcentaje por Fila", "Porcentaje por Columna"
        ])
        
        with tab1:
            st.dataframe(tablas_estaciones_fatalidad['absoluta'], use_container_width=True)
        with tab2:
            st.dataframe(tablas_estaciones_fatalidad['porcentaje_total'], use_container_width=True)
        with tab3:
            st.dataframe(tablas_estaciones_fatalidad['condicional_filas'], use_container_width=True)
        with tab4:
            st.dataframe(tablas_estaciones_fatalidad['condicional_columnas'], use_container_width=True)
else:
    tabla_estaciones = utils.analizar_frecuencias(df, 'season', excluir_desconocido=True)
    if not tabla_estaciones.empty:
        st.dataframe(tabla_estaciones, use_container_width=True)

st.markdown("""
    <div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
    La estación del año con más ataques de tiburón registrados es el invierno. Esto puede deberse a que durante esa época la noche suele ser más duradera, cuando los tiburones son mucho más activos, además que en ciertos lugares del hemisferio sur, como lo es Australia, su verano ocurre de diciembre a marzo, donde en otros lugares sería invierno, haciendo que mucha más población se encuentre en las playas, aumentando la posibilidad de algún ataque.

    Después del invierno, las estaciones con más ataques registrados son otoño y verano, siendo primavera la estación con menos ataques registrados.
            
    Cuando se condiciona esta variable con la variable de fatalidad, podemos ver que la estación con mayor cantidad de ataques de tiburones con resultados fatales es el verano, con 306 ataques registrados (un 6,12 % del total). Las demás estaciones en orden de ataques fatales son: otoño con 289 ataques (4,52%), invierno con 278 ataques (5,56%) y por último primavera, con 226 ataques mortales (4,52%).
        
    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Estadísticas Descriptivas")