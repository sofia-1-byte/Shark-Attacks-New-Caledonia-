import streamlit as st
import pandas as pd
from utils import _conectar_bd 

# Ya no necesitamos definir CONFIG ni _conectar_bd aquí

@st.cache_data
def obtener_ataques_por_estacion():
    """
    Obtiene la distribución de ataques de tiburones por estación del año desde la vista predefinida.
    

    Returns:
        pd.DataFrame: DataFrame con las columnas:
            - estacion: Nombre de la estación (Primavera, Verano, Otoño, Invierno, Desconocido)
            - cantidad_ataques: Número total de ataques en esa estación
            - porcentaje: Porcentaje que representa cada estación sobre el total de ataques
    """
    try:
        conn = _conectar_bd() 
        if not conn:
            return pd.DataFrame()
        
        consulta = "SELECT * FROM vista_ataques_por_estacion;"
        resultado = pd.read_sql_query(consulta, conn)
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"error en consulta de estaciones: {e}")
        return pd.DataFrame()

@st.cache_data
def obtener_top5_actividades_fatales():
    """
    Recupera las 5 actividades con mayor número de ataques fatales desde la vista especializada.

    Returns:
        pd.DataFrame: DataFrame con las columnas:
            - actividad: Tipo de actividad realizada durante el ataque (surf, natación, buceo, etc.)
            - ataques_fatales: Cantidad de ataques mortales asociados a cada actividad
    """
    try:
        conn = _conectar_bd()  
        if not conn:
            return pd.DataFrame()
        
        consulta = "SELECT * FROM vista_top5_actividades_fatales;"
        resultado = pd.read_sql_query(consulta, conn)
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"error en consulta de actividades fatales: {e}")
        return pd.DataFrame()

@st.cache_data
def obtener_ataques_por_fase_lunar():
    """
    Obtiene la distribución de ataques según las fases lunares desde la vista correspondiente.

    Returns:
        pd.DataFrame: DataFrame con las columnas:
            - fase_lunar: Nombre de la fase lunar en el momento del ataque
            - cantidad_ataques: Número de ataques ocurridos durante esa fase lunar
            - porcentaje: Porcentaje que representa cada fase lunar sobre el total de ataques
    """
    try:
        conn = _conectar_bd()  
        if not conn:
            return pd.DataFrame()
        
        consulta = "SELECT * FROM vista_ataques_por_fase_lunar;"
        resultado = pd.read_sql_query(consulta, conn)
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"error en consulta de fases lunares: {e}")
        return pd.DataFrame()

@st.cache_data
def obtener_especies_conservacion():
    """
    Recupera información sobre las especies de tiburones y su estado de conservación desde la vista.
    
    Returns:
        pd.DataFrame: DataFrame con información detallada que incluye:
            - species: Nombre de la especie de tiburón
            - conservation_status: Estado de conservación (En Peligro, Vulnerable, etc.)
            - Otros datos relevantes sobre la distribución y frecuencia de ataques por especie
    """
    try:
        conn = _conectar_bd() 
        if not conn:
            return pd.DataFrame()
        
        consulta = "SELECT * FROM vista_especies_conservacion;"
        resultado = pd.read_sql_query(consulta, conn)
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"error en consulta de especies: {e}")
        return pd.DataFrame()

@st.cache_data
def obtener_ataques_fatales_por_decada():
    """
    Obtiene la cantidad de ataques fatales agrupados por década desde la vista designada.
    
    Returns:
        pd.DataFrame: DataFrame con las columnas:
            - decada: Rango de años representado por la década (ej: 1990-1999)
            - ataques_fatales: Número total de ataques mortales registrados en esa década
    """
    try:
        conn = _conectar_bd() 
        if not conn:
            return pd.DataFrame()
        
        consulta = "SELECT * FROM vista_ataques_fatales_por_decada;"
        resultado = pd.read_sql_query(consulta, conn)
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"error en consulta de decadas: {e}")
        return pd.DataFrame()

def mostrar_consulta(funcion_consulta, titulo, descripcion, codigo_sql):
    """  
    Función de utilidad que estandariza la visualización de consultas en la aplicación, mostrando
    tanto los resultados tabulares como el código SQL subyacente, junto con métricas básicas.
    
    Args:
        funcion_consulta (callable): Función que ejecuta la consulta y retorna un DataFrame
        titulo (str): Título descriptivo de la sección que se mostrará en la interfaz
        descripcion (str): Explicación detallada del propósito y significado de la consulta
        codigo_sql (str): Código SQL completo de la consulta para fines educativos y de transparencia
    
    """
    st.markdown(f"### {titulo}")
    st.write(descripcion)
    
    # ejecutar consulta
    with st.spinner("ejecutando consulta..."):
        df = funcion_consulta()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        # mostrar estadisticas basicas
        if len(df) > 0:
            st.write(f"**total de registros:** {len(df)}")
            
        # mostrar codigo sql
        with st.expander("ver consulta sql"):
            st.code(codigo_sql, language="sql")
    else:
        st.warning("no se encontraron datos para esta consulta")
    
    st.markdown("---")