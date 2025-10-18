import streamlit as st
from twisted.web.http import datetimeToString

import utils

# Configuracion de la página
st.set_page_config(
    page_title="Shark_attack",
    page_icon="📄",
    layout="centered"
)

# Titulo principal
st.title("Shark Attack")

# Seccion de justificación
st.header("Objetivos del Proyecto")

st.markdown("""
Objetivo General

    Determinar los patrones descriptivos de riesgo asociados a los incidentes de tiburones en Nueva Caledonia. Esto se logrará usando las características de los ataques, sus víctimas y el entorno (actividad, ubicación y temporalidad), a través de métodos de estadística descriptiva para generar información preventiva.

Objetivos Específicos

    Analizar la letalidad de los ataques para establecer la proporción porcentual exacta de incidentes clasificados como fatales dentro del total de registros.

    Evaluar el riesgo por actividad para identificar, mediante la frecuencia absoluta y relativa, la actividad (activity) que concentra el mayor número de ataques.

    Rankear los Paises que registran la más alta frecuencia de ataques.

    Caracterizar el perfil de la víctima mediante el cálculo de la media y la mediana de la edad y la distribución de frecuencias para la variable sexo.

    Análisar las tablas de frecuencias agrupadas por estación y versus fatalidad del ataque, buscando patrones de ocurrencia.

    Determinar si existe una mayor proporción de fatalidad al analizar los datos de la actividad (activity) vs la gravedad del incidente (is_fatal).
""")



# Sidebar con información adicional
tabla = "shark_attacks"


#Pedimos la tabla que quiere visualizar el usuario
with st.sidebar:
    tabla = utils.obtener_tablas_disponibles()
    st.write("""ingresa la tabla""")
    tabla = st.selectbox(
        "Seleccione una tabla",
        tabla,
    )


    st.header(" Datos en Tiempo Real")
    if st.button("Cargar datos actualizados"):
        with st.spinner("Cargando datos..."):
            datos = utils.cargar_datos(tabla)

            if datos is not None:
                st.success(f" Se cargaron {len(datos)} registros")
                st.metric("Total de registros", len(datos))

            else:
                st.error("Error al cargar los datos")



    st.markdown("---")
    st.info("""
    **Configuración actual:**
    - Base de datos: SQLite
    - Tabla principal: shark_attack
    - Última actualización: Automática
    """)

##Hace falta corregír el checkbox que no funciona
if st.checkbox("Mostrar vista previa de los datos"):
    st.write(datos.head(5))



# Pie de página
st.markdown("---")
st.caption("")

