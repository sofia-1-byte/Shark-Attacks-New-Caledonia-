import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import os
from scipy import stats


current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "bbdd", "shark_attacks.db")

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
    Esta función intenta conectarse a la base de datos usando la ruta definida en CONFIG.
    Es una función interna utilizada por otras funciones para obtener conexiones a la BDD.
    
    Returns:
        Optional[sqlite3.Connection]: Objeto de conexión a la base de datos si es exitoso, 
        None si ocurre algún error durante la conexión.
        
    """
    try:
        return sqlite3.connect(CONFIG["base_de_datos"])
    except Exception as e:
        st.error(f"error conectando a la base de datos: {e}")
        return None

@st.cache_data(show_spinner="cargando y limpiando datos...")
def load_and_clean_data() -> pd.DataFrame:
    """
    Realiza las siguientes operaciones principales:
    1. Conecta a la bbdd y ejecuta una consulta joint entre tablas de ataques, tiburones y estado de conservación
    2. Aplica transformaciones y limpieza a las columnas:
       - Normaliza valores fatales usando FATAL_MAPPING
       - Normaliza géneros usando SEX_MAPPING
       - Limpia y estandariza actividades, fases lunares y estaciones
       - Convierte y valida edades, filtrando valores fuera de rango [0, 100]
    3. Cachea los resultados para mejorar rendimiento en aplicaciones Streamlit
    
    Returns:
        pd.DataFrame: DataFrame con los datos limpios y normalizados, o DataFrame vacío si hay error.
        
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
        
        
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['age'] = df['age'].apply(lambda x: x if pd.notna(x) and 0 <= x <= 100 else np.nan)
        
        return df
        
    except Exception as e:
        st.error(f"error critico en carga de datos: {e}")
        return pd.DataFrame()

def analizar_frecuencias(_df: pd.DataFrame, columna: str, excluir_desconocido: bool = True) -> pd.DataFrame:
    """
    Calcula distribuciones de frecuencia absoluta y relativa para una columna determinada,
    permitiendo excluir valores desconocidos para focarse en datos válidos. Es útil para
    entender la distribución de variables como actividad, país, especie, etc.
    
    Args:
        _df (pd.DataFrame): DataFrame con los datos de ataques de tiburones
        columna (str): Nombre de la columna categórica a analizar
        excluir_desconocido (bool): Si True, excluye la categoría 'Desconocido' del análisis
    
    Returns:
        pd.DataFrame: DataFrame con columnas:
            - Categoria: Valores únicos de la columna analizada
            - Frecuencia Absoluta: Conteo de ocurrencias
            - Frecuencia Relativa: Proporción entre 0 y 1
            - Frecuencia Relativa %: Porcentaje con 2 decimales
            
    """
    if columna not in _df.columns:
        return pd.DataFrame()

    df_filtrado = _df[_df[columna] != 'Desconocido'] if excluir_desconocido else _df

    if df_filtrado.empty:
        return pd.DataFrame()

    # Frecuencias basicas
    frecuencias = df_filtrado[columna].value_counts(dropna=False)
    total = frecuencias.sum()

    # Crear dataframe base
    resultado = pd.DataFrame({
        'Categoria': frecuencias.index,
        'Frecuencia Absoluta': frecuencias.values,
        'Frecuencia Relativa': (frecuencias.values / total).round(4),
        'Frecuencia Relativa %': (frecuencias.values / total * 100).round(2)
    }).sort_values('Frecuencia Absoluta', ascending=False).reset_index(drop=True)

    return resultado

def crear_tablas_doble_entrada(_df: pd.DataFrame, fila: str, columna: str) -> Dict[str, pd.DataFrame]:
    """
    Genera cuatro tipos de tablas para analizar la relación entre dos variables:
    1. Frecuencias absolutas
    2. Porcentajes sobre el total general
    3. Distribuciones condicionales por filas (cada fila suma 100%)
    4. Distribuciones condicionales por columnas (cada columna suma 100%)
    
    Args:
        _df (pd.DataFrame): DataFrame con los datos de ataques
        fila (str): Nombre de la variable para las filas de la tabla
        columna (str): Nombre de la variable para las columnas de la tabla
    
    Returns:
        Dict[str, pd.DataFrame]: Diccionario con cuatro tablas y sus explicaciones:
            - 'absoluta': Frecuencias absolutas de casos
            - 'porcentaje_total': Porcentajes sobre el total general
            - 'condicional_filas': Distribución por filas (100% por fila)
            - 'condicional_columnas': Distribución por columnas (100% por columna)
            - 'explicacion': Descripciones de cada tipo de tabla       
    """
    if fila not in _df.columns or columna not in _df.columns:
        return {}

    df_filtrado = _df[(_df[fila] != 'Desconocido') & (_df[columna] != 'Desconocido')].copy()

    if df_filtrado.empty:
        return {}

    # Tabla absoluta basica
    tabla_absoluta = pd.crosstab(df_filtrado[fila], df_filtrado[columna], margins=True, margins_name="Total")
    total_general = tabla_absoluta.loc['Total', 'Total']

    # Distribuciones porcentuales
    tabla_porcentaje_total = (tabla_absoluta / total_general * 100).round(2)

    # Distribuciones condicionales por filas (cada fila suma 100%)
    tabla_condicional_filas = tabla_absoluta.copy().drop('Total', axis=1).drop('Total', axis=0)
    tabla_condicional_filas = tabla_condicional_filas.div(tabla_condicional_filas.sum(axis=1), axis=0) * 100
    tabla_condicional_filas = tabla_condicional_filas.round(2)

    # Distribuciones condicionales por columnas (cada columna suma 100%)
    tabla_condicional_columnas = tabla_absoluta.copy().drop('Total', axis=1).drop('Total', axis=0)
    tabla_condicional_columnas = tabla_condicional_columnas.div(tabla_condicional_columnas.sum(axis=0), axis=1) * 100
    tabla_condicional_columnas = tabla_condicional_columnas.round(2)

    # Agregar totales a las tablas condicionales
    tabla_condicional_filas['Total'] = 100.0
    tabla_condicional_columnas.loc['Total'] = 100.0

    return {
        'absoluta': tabla_absoluta,
        'porcentaje_total': tabla_porcentaje_total,
        'condicional_filas': tabla_condicional_filas,
        'condicional_columnas': tabla_condicional_columnas,
        'explicacion': {
            'absoluta': "Frecuencias absolutas de casos",
            'porcentaje_total': "Porcentaje sobre el total general (base: 100% = total de casos)",
            'condicional_filas': f"Distribución condicional de {columna} dado {fila} - cada fila suma 100%",
            'condicional_columnas': f"Distribución condicional de {fila} dado {columna} - cada columna suma 100%"
        }
    }


def obtener_estadisticas_completas(_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula estadísticas descriptivas completas.
      
    Args:
        _df (pd.DataFrame): DataFrame con los datos de ataques de tiburones
    
    Returns:
        Dict[str, Any]: Diccionario con tres componentes:
            - 'metricas_basicas': Total registros, conteos fatales, tasa fatalidad, etc.
            - 'estadisticas_edad': DataFrame con stats descriptivas por tipo de caso
            - 'tasas_actividad': DataFrame con tasas de fatalidad por actividad ordenadas
    
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


def cargar_datos_y_estadisticas():
    """
    Función principal que carga los datos y calcula todas las estadísticas necesarias.
    
    Returns:
        tuple: Tupla con dos elementos:
            - pd.DataFrame: DataFrame con todos los datos limpios
            - dict: Diccionario con todas las estadísticas calculadas
    """
    df = load_and_clean_data()
    estadisticas = obtener_estadisticas_completas(df) if not df.empty else {}
    return df, estadisticas