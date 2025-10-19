import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import os
from scipy import stats
from PIL import Image

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "bbdd", "shark_attacks.db")

CONFIG = {
    "base_de_datos": db_path,
    "tabla_ataques": "shark_attackdatos",
    "tabla_tiburones": "SHARKS", 
    "tabla_conservacion": "conservation_status"
}

FATAL_MAPPING = {
    'Y': 'Fatal', 'YES': 'Fatal', '1': 'Fatal',
    'N': 'No Fatal', 'NO': 'No Fatal', '0': 'No Fatal',
    'NAN': 'Desconocido', 'NONE': 'Desconocido', 'UNKNOWN': 'Desconocido',
    'DESCONOCIDO': 'Desconocido'
}

SEX_MAPPING = {
    'M': 'Masculino', 'F': 'Femenino', 
    'N': 'Desconocido', 'NAN': 'Desconocido'
}

UNKNOWN_VALUES = {'nan', 'none', 'unknown', 'desconocido', ''}

def _conectar_bd() -> Optional[sqlite3.Connection]:
    """
    establece conexion con la base de datos sqlite
    returns:
        connection: objeto de conexion a la base de datos o none si hay error
    """
    try:
        return sqlite3.connect(CONFIG["base_de_datos"])
    except Exception as e:
        st.error(f"error conectando a la base de datos: {e}")
        return None

@st.cache_data(show_spinner="cargando y limpiando datos...")
def load_and_clean_data() -> pd.DataFrame:
    """
    carga los datos desde la base de datos y realiza procesos de limpieza
    returns:
        dataframe: dataframe con los datos limpios o dataframe vacio si hay error
    """
    try:
        conn = _conectar_bd()
        if not conn:
            return pd.DataFrame()
            
        query = f"""
        SELECT 
            a.is_fatal, 
            a.activity, 
            a.moon_phase, 
            a.age, 
            a.sex, 
            a.season, 
            a.day_part,
            a.country, 
            a.species,
            s.conservation_status,
            cs.cat as conservation_description
        FROM {CONFIG['tabla_ataques']} a
        LEFT JOIN {CONFIG['tabla_tiburones']} s ON a.species = s.id
        LEFT JOIN {CONFIG['tabla_conservacion']} cs ON s.conservation_status = cs.id_long
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return df

        df['is_fatal_cat'] = df['is_fatal'].map(FATAL_MAPPING).fillna('Desconocido')
        df['sex'] = df['sex'].map(SEX_MAPPING).fillna('Desconocido')
        
        df['activity'] = df['activity'].astype(str).str.upper().str.strip()
        df.loc[df['activity'].str.upper().isin(UNKNOWN_VALUES), 'activity'] = 'Desconocido'
        df.loc[df['activity'].isna(), 'activity'] = 'Desconocido'
        
        df['moon_phase'] = df['moon_phase'].astype(str).str.upper().str.strip()
        df.loc[df['moon_phase'].str.upper().isin(UNKNOWN_VALUES), 'moon_phase'] = 'Desconocido'
        df.loc[df['moon_phase'].isna(), 'moon_phase'] = 'Desconocido'
        
        df['season'] = df['season'].astype(str).str.upper().str.strip()
        df.loc[df['season'].str.upper().isin(UNKNOWN_VALUES), 'season'] = 'Desconocido'
        df.loc[df['season'].isna(), 'season'] = 'Desconocido'
        
        df['day_part'] = df['day_part'].astype(str).str.upper().str.strip()
        df.loc[df['day_part'].str.upper().isin(UNKNOWN_VALUES), 'day_part'] = 'Desconocido'
        df.loc[df['day_part'].isna(), 'day_part'] = 'Desconocido'
        
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['age'] = df['age'].apply(lambda x: x if pd.notna(x) and 0 <= x <= 100 else np.nan)
        
        return df
        
    except Exception as e:
        st.error(f"error critico en carga de datos: {e}")
        return pd.DataFrame()

def analizar_frecuencias(_df: pd.DataFrame, columna: str, excluir_desconocido: bool = True) -> pd.DataFrame:
    """
    analiza las frecuencias de valores en una columna categorica
    parametros:
        _df: dataframe - dataframe con los datos
        columna: str - nombre de la columna a analizar
        excluir_desconocido: bool - si es verdadero excluye valores desconocidos
    returns:
        dataframe: tabla con frecuencias absolutas y relativas
    """
    if columna not in _df.columns:
        return pd.DataFrame()
    
    df_filtrado = _df[_df[columna] != 'Desconocido'] if excluir_desconocido else _df
    
    if df_filtrado.empty:
        return pd.DataFrame()
    
    frecuencias = df_filtrado[columna].value_counts(dropna=False)
    total = frecuencias.sum()
    
    return pd.DataFrame({
        'Categoria': frecuencias.index,
        'Frecuencia Absoluta': frecuencias.values,
        'Frecuencia Relativa': (frecuencias.values / total).round(4),
        'Frecuencia Relativa %': (frecuencias.values / total * 100).round(2)
    }).sort_values('Frecuencia Absoluta', ascending=False).reset_index(drop=True)

def crear_tablas_doble_entrada(_df: pd.DataFrame, fila: str, columna: str) -> Dict[str, pd.DataFrame]:
    """
    crea tablas de doble entrada entre dos variables
    parametros:
        _df: dataframe - dataframe con los datos
        fila: str - nombre de la variable para las filas
        columna: str - nombre de la variable para las columnas
    returns:
        dict: diccionario con diferentes tipos de tablas de contingencia
    """
    if fila not in _df.columns or columna not in _df.columns:
        return {}
    
    df_filtrado = _df[(_df[fila] != 'Desconocido') & (_df[columna] != 'Desconocido')].copy()
    
    if df_filtrado.empty:
        return {}
    
    tabla_absoluta = pd.crosstab(df_filtrado[fila], df_filtrado[columna], margins=True, margins_name="Total")
    total_general = tabla_absoluta.loc['Total', 'Total']
    
    return {
        'absoluta': tabla_absoluta,
        'rel_total': (tabla_absoluta / total_general * 100).round(2),
        'rel_fila': tabla_absoluta.div(tabla_absoluta.sum(axis=1), axis=0).round(4) * 100,
        'rel_columna': tabla_absoluta.div(tabla_absoluta.sum(axis=0), axis=1).round(4) * 100
    }


def obtener_estadisticas_completas(_df: pd.DataFrame) -> Dict[str, Any]:
    """
    calcula estadisticas descriptivas y metricas del dataset
    parametros:
        _df: dataframe - dataframe con los datos de ataques
    returns:
        dict: diccionario con metricas basicas, estadisticas de edad y tasas por actividad
    """
    ataques_conocidos = _df['is_fatal_cat'].isin(['Fatal', 'No Fatal']).sum()
    tasa_fatalidad = (_df['is_fatal_cat'].eq('Fatal').sum() / ataques_conocidos * 100) if ataques_conocidos > 0 else 0
    
    metricas_basicas = {
        'total_registros': len(_df),
        'ataques_fatales': _df['is_fatal_cat'].eq('Fatal').sum(),
        'ataques_no_fatales': _df['is_fatal_cat'].eq('No Fatal').sum(),
        'tasa_fatalidad': tasa_fatalidad,
        'edad_promedio': _df['age'].mean(),
        'actividad_mas_comun': _df['activity'].mode().iloc[0] if not _df['activity'].mode().empty else 'N/A'
    }
    
    estadisticas_edad = pd.DataFrame()
    if 'age' in _df.columns and not _df['age'].isna().all():
        def _calcular_stats(serie):
            if serie.empty:
                return {k: np.nan for k in ['Media', 'Mediana', 'Moda', 'Desviacion', 'Asimetria', 'Curtosis']}
            
            return {
                'Media': serie.mean(),
                'Mediana': serie.median(),
                'Moda': serie.mode().iloc[0] if not serie.mode().empty else np.nan,
                'Desviacion': serie.std(),
                'Asimetria': stats.skew(serie) if len(serie) > 2 else np.nan,
                'Curtosis': stats.kurtosis(serie) if len(serie) > 3 else np.nan
            }
        
        df_edad = _df[~_df['age'].isna()].copy()
        edad_total = df_edad['age'].dropna()
        edad_fatal = df_edad[df_edad['is_fatal_cat'] == 'Fatal']['age'].dropna()
        edad_no_fatal = df_edad[df_edad['is_fatal_cat'] == 'No Fatal']['age'].dropna()
        
        estadisticas_edad = pd.DataFrame({
            'Todos los Casos': _calcular_stats(edad_total),
            'Casos Fatales': _calcular_stats(edad_fatal),
            'Casos No Fatales': _calcular_stats(edad_no_fatal)
        }).round(2)
    
    tasas_actividad = pd.DataFrame()
    df_actividad = _df[(_df['activity'] != 'Desconocido') & (_df['is_fatal_cat'].isin(['Fatal', 'No Fatal']))].copy()
    
    if not df_actividad.empty:
        tabla_actividad = pd.crosstab(df_actividad['activity'], df_actividad['is_fatal_cat'])
        tabla_actividad['Total'] = tabla_actividad.sum(axis=1)
        tabla_actividad['Tasa Fatalidad %'] = (tabla_actividad['Fatal'] / tabla_actividad['Total'] * 100).round(2)
        tasas_actividad = tabla_actividad.sort_values('Tasa Fatalidad %', ascending=False)
    
    return {
        'metricas_basicas': metricas_basicas,
        'estadisticas_edad': estadisticas_edad,
        'tasas_actividad': tasas_actividad
    }

# funciones de sql

@st.cache_data
def obtener_ataques_por_estacion():
    """
    obtiene los ataques por estacion del año usando la vista
    returns:
        dataframe: con columnas [estacion, cantidad_ataques, porcentaje]
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
    obtiene el top 5 de actividades con mas ataques fatales usando la vista
    returns:
        dataframe: con columnas [actividad, ataques_fatales]
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
    obtiene los ataques por fase lunar usando la vista
    returns:
        dataframe: con columnas [fase_lunar, cantidad_ataques, porcentaje]
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
    obtiene las especies implicadas en ataques con su categoria de conservacion usando la vista
    returns:
        dataframe: con informacion de especies y estado de conservacion
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
    obtiene el numero de ataques fatales por decada usando la vista
    returns:
        dataframe: con columnas [decada, ataques_fatales]
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

def cargar_logo(nombre_logo):
    """
    carga un logo desde diferentes rutas posibles
    """
    try:
        # Agrega aquí la ruta exacta donde están tus logos
        rutas = [
            f"logos/{nombre_logo}", 
            f"./logos/{nombre_logo}", 
            f"C:/Users/PC/OneDrive/Documents/Shark-Attacks-Trabajo-Final/strimlit/logo/{nombre_logo}",
        ]
        
        for ruta in rutas:
            if os.path.exists(ruta):
                return Image.open(ruta)
        
        return None
        
    except Exception as e:
        return None

def mostrar_header():
    """muestra el header con ambos logos"""
    # cargar logos
    logo_ucv = cargar_logo("UCV.png") 
    logo_eeca = cargar_logo("EECA.png")  
    
    # crear header con dos columnas para los logos
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if logo_ucv:
            st.image(logo_ucv, width=100)
    
    with col2:
        if logo_eeca:
            st.image(logo_eeca, width=100)
    
    st.markdown("---")


def cargar_datos_y_estadisticas():
    """
    carga los datos y calcula las estadisticas necesarias
    returns:
        tuple: dataframe con datos y diccionario con estadisticas
    """
    df = load_and_clean_data()
    estadisticas = obtener_estadisticas_completas(df) if not df.empty else {}
    return df, estadisticas

def mostrar_consulta(funcion_consulta, titulo, descripcion, codigo_sql):
    """muestra una consulta sql con sus resultados y codigo
    argumentos:
        funcion_consulta: funcion - funcion que ejecuta la consulta y retorna un dataframe
        titulo: str - titulo de la seccion
        descripcion: str - descripcion de la consulta
        codigo_sql: str - codigo sql de la consulta
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

def grafico_pie(columna: str, excluir: bool = False) :
    """ Genera un gráfico de pie según las proporciones de las columnas de la
    Parameters:
        columna (str): columna de tablas
        excluir (bool, optional): decidir si se excluyen valores desconocidos

    """

    ##Cargar el dataframe.

    df = load_and_clean_data()

    ##Analizar frecuencias de los fatales
    df_grafico = analizar_frecuencias(df, columna, excluir)
    #print(df_fatals.head())

    ##Condicionar titulos para el gráfico de pie según las variables
    if columna == "activity":
        title = "Proporcion de ataques según actividad"
    elif columna == "is_fatal_cat":
        title = "Proporción de ataques según fatalidad"
    elif columna == "season":
        title = "Proporción de ataques según Temporada"
    elif columna == "sex":
        title = "Proporción de ataques según sexo de las víctimas"
    elif columna == "species":
        title = "Proporción de ataques según la Especie de Tiburón"
    elif columna == "day_part":
        title = "Proporción de ataques según el horario"


    ## Construcción del gráfico
    pie_grafico = px.pie(df_grafico, values='Frecuencia Absoluta', names='Categoria',
                  title=title)
    return pie_grafico

