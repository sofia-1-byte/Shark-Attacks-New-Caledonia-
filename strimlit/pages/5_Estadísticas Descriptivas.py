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

    Si condicionamos la tabla de actividades por fatalidad podemos observar que la actividad más mortal es nadar, con 324 encuentros (6,48% de los ataques totales). A este le siguen: bodyboarding, con 313 víctimas fatales (6,26%), y pescar, con 164 fatalidades (3,28%). En cambio, las actividades menos fatales son remar, surfskiing y boogie boarding, con 0, 0 y 2 ataques fatales respectivamente, representando solo el 0,04% de los ataques totales.

    Si miramos la tabla condicionada en porcentaje por fila, las actividades más mortales son: caer a bordo de una embarcación (con un 75% de fatalidad),  bañarse (42,42% de fatalidad) y nadar (37,5% de fatalidad). Mientras que, las actividades menos fatales son remar (100% de no ser fatal),  el surf skiing (con otro 100% de no fatalidad) y el boogie boarding (95% de no ser fatal).

    Si se usa la función de porcentaje por columnas, se puede apreciar que de los ataques fatales, los más mortales son: nadar (29,48%),  el bodyboarding (28,48%) y pescar (14,92%). Por su parte, la mayoría de los ataques no letales son por parte de: surfear (25,6%), pescar (20,76%) y del bodyboarding (16,99%).

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

    Cuando colocamos la opción de porcentaje por filas, se puede ver que en un gran número de países y/o territorios como pueden ser Samoa Americana, Aruba y Bangladesh, la fatalidad de los ataques de tiburones es del 100%. Mientras que, en otros lugares como Argentina, las islas Azores o Canadá, se puede apreciar que la tasa de ataques no fatales es del 100%.

    Si se coloca la opción de porcentaje por columnas, se observa que los países con la mayor cantidad de ataques letales son: Australia (22,29 % de todos los ataques fatales), EE UU (17,11%) y Sudáfrica (10,01%).  De igual manera, los países que acaparan la mayor cantidad de ataques no fatales son: EE UU (44,82%), Australia (20,53%) y Sudáfrica (10,4%).

            
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

 Si se ve en porcentaje por filas, la tasa de mortalidad de cada grupo es la siguiente; el 26,71% de los ataques al grupo de mayores de 60 años son fatales, el 23,17% al grupo de 46 a 60 años, el 22,91% a los de entre 19 a 30 años, el 20,91% al grupo de 31 a 45 años, y por último, un 18,13% al grupo de las personas entre 0 a 18 años.

 En porcentaje por columnas, se puede observar que los ataques fatales se encuentran repartidos así: 38,58% de parte del grupo de 19 a 30 años, un 17,93% del grupo de 31 a 45 años, un 16,92% del grupo de 0 a 18 años, un 14,1% del grupo de 46 a 60 años, y un 12,47% de parte del grupo de mayores de 60 años. Si hablamos de los ataques no fatales, se puede ver que de estos, el 36,57% pertenece al grupo de víctimas de entre 19 a 30 años (siendo la gran mayoría), el 19,09% son del grupo de 31 a 45 años, 21,53% representa al grupo de 0 a 18 años, el 13,17% al grupo de de 46 a 60 años, y por ultimo, solo un 9,64% son del grupo de mayores de 60 años

            
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
        
    Al usar la opción de porcentaje por fila, se puede apreciar que la mortalidad de cada temporada es la siguiente: el verano es la temporada más fatal, con un 26,42% de mortalidad, le sigue el otoño, con 23,63% de mortalidad, luego la primavera, con 19,58% de fatalidad, y por ultimo esta el invierno, con un 18,96% de fatalidad.

    En porcentaje por columna, se observa que de los ataques fatales, un 27,84% de ellos corresponden a los ocurridos en verano, 26,3% a los de otoño, un 25,3% a los de invierno y un 20,56% a los de primavera. Del otro extremo, de los ataques no fatales, un 30,45% son de la estación de invierno, 23,94% de otoño, un 23,78% de primavera, y un 21,83% de estos ataques ocurren en el verano.
        
    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Estadísticas Descriptivas")