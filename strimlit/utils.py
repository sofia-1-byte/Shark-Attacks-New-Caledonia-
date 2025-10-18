import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import os
from scipy import stats

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "..", "bbdd", "shark_attacks.db")

CONFIG = {
    "base_de_datos": db_path,
    "tabla": "shark_attackdatos"
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

@st.cache_resource
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
    carga los datos desde la base de datos y realiza proesos de limpieza
    returns:
        dataframe: dataframe con los datos limpios o dataframe vacio si hay error
    """
    try:
        conn = _conectar_bd()
        if not conn:
            return pd.DataFrame()
            
        query = f"SELECT is_fatal, activity, moon_phase, age, sex, season, day_part, country, species FROM {CONFIG['tabla']}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.warning("no se pudieron cargar datos de la base de datos")
            return pd.DataFrame()
        
        categorical_cols = ['activity', 'country', 'season', 'day_part', 'moon_phase', 'species']
        
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna('Desconocido').astype(str).str.strip().str.title()
                df[col] = df[col].replace({'Nan': 'Desconocido', 'None': 'Desconocido', 'Unknown': 'Desconocido', '': 'Desconocido'})
        
        if 'sex' in df.columns:
            df['sex'] = df['sex'].fillna('Desconocido').astype(str).str.strip().str.upper()
            df['sex'] = df['sex'].replace(SEX_MAPPING)
        
        df['is_fatal'] = df['is_fatal'].fillna('Desconocido').astype(str).str.strip().str.upper()
        df['is_fatal_cat'] = df['is_fatal'].replace(FATAL_MAPPING)
        df['is_fatal_num'] = df['is_fatal_cat'].map({'Fatal': 1, 'No Fatal': 0, 'Desconocido': pd.NA})
        
        if 'age' in df.columns:
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
        
        return df
        
    except Exception as e:
        st.error(f"error critico en carga de datos: {e}")
        return pd.DataFrame()

def analizar_frecuencias(_df: pd.DataFrame, columna: str, excluir_desconocido: bool = True) -> pd.DataFrame:
    """
    analiza las frecuencias de valores en una columna categorica
    parametros:
        _df: dataframe con los datos
        columna: nombre de la columna a analizar
        excluir_desconocido: si es verdadero excluye valores desconocidos
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
        _df: dataframe con los datos
        fila: nombre de la variable para las filas
        columna: nombre de la variable para las columnas
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
        _df: dataframe con los datos de ataques
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