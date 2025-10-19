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

def crear_vistas():
    """
    crea las vistas sql en la base de datos para las consultas frecuentes
    returns:
        bool: True si se crearon las vistas correctamente, False si hubo error
    """
    try:
        conn = _conectar_bd()
        if not conn:
            return False
        
        vistas_sql = [
            """
            CREATE VIEW IF NOT EXISTS vista_ataques_por_estacion AS
            SELECT 
                season as estacion,
                COUNT(*) as cantidad_ataques,
                ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shark_attackdatos 
                WHERE season IS NOT NULL AND season != 'Desconocido')), 2) as porcentaje
            FROM shark_attackdatos 
            WHERE season IS NOT NULL AND season != 'Desconocido'
            GROUP BY season
            ORDER BY cantidad_ataques DESC;
            """,
            """
            CREATE VIEW IF NOT EXISTS vista_top5_actividades_fatales AS
            SELECT 
                activity as actividad,
                COUNT(*) as ataques_fatales
            FROM shark_attackdatos 
            WHERE is_fatal = 'Y' 
                AND activity IS NOT NULL 
                AND activity != 'Desconocido'
                AND activity != ''
            GROUP BY activity
            ORDER BY ataques_fatales DESC
            LIMIT 5;
            """,
            """
            CREATE VIEW IF NOT EXISTS vista_ataques_por_fase_lunar AS
            SELECT 
                CASE 
                    WHEN moon_phase IS NULL OR moon_phase = '' OR moon_phase = 'Desconocido' THEN 'Desconocido'
                    ELSE moon_phase
                END as fase_lunar,
                COUNT(*) as cantidad_ataques,
                ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shark_attackdatos)), 2) as porcentaje
            FROM shark_attackdatos 
            GROUP BY 
                CASE 
                    WHEN moon_phase IS NULL OR moon_phase = '' OR moon_phase = 'Desconocido' THEN 'Desconocido'
                    ELSE moon_phase
                END
            ORDER BY cantidad_ataques DESC;
            """,
            """
            CREATE VIEW IF NOT EXISTS vista_especies_conservacion AS
            SELECT DISTINCT
                a.species as especie,
                s.conservation_status as categoria_conservacion,
                cs.cat as descripcion_completa
            FROM shark_attackdatos a
            INNER JOIN SHARKS s ON a.species = s.id
            INNER JOIN conservation_status cs ON s.conservation_status = cs.id_long
            WHERE a.species IS NOT NULL 
                AND a.species != 'Desconocido'
                AND a.species != '';
            """,
            """
            CREATE VIEW IF NOT EXISTS vista_ataques_fatales_por_decada AS
            SELECT 
                CASE 
                    WHEN year BETWEEN 1900 AND 1909 THEN '1900-1909'
                    WHEN year BETWEEN 1910 AND 1919 THEN '1910-1919'
                    WHEN year BETWEEN 1920 AND 1929 THEN '1920-1929'
                    WHEN year BETWEEN 1930 AND 1939 THEN '1930-1939'
                    WHEN year BETWEEN 1940 AND 1949 THEN '1940-1949'
                    WHEN year BETWEEN 1950 AND 1959 THEN '1950-1959'
                    WHEN year BETWEEN 1960 AND 1969 THEN '1960-1969'
                    WHEN year BETWEEN 1970 AND 1979 THEN '1970-1979'
                    WHEN year BETWEEN 1980 AND 1989 THEN '1980-1989'
                    WHEN year BETWEEN 1990 AND 1999 THEN '1990-1999'
                    WHEN year BETWEEN 2000 AND 2009 THEN '2000-2009'
                    WHEN year BETWEEN 2010 AND 2019 THEN '2010-2019'
                    WHEN year BETWEEN 2020 AND 2025 THEN '2020-2025'
                    ELSE 'Otra'
                END as decada,
                COUNT(*) as ataques_fatales
            FROM shark_attackdatos 
            WHERE is_fatal = 'Y' 
                AND year IS NOT NULL
            GROUP BY decada
            ORDER BY MIN(year);
            """
        ]
        
        for vista_sql in vistas_sql:
            conn.execute(vista_sql)
        
        conn.commit()
        conn.close()
        st.success("Vistas creadas exitosamente")
        return True
        
    except Exception as e:
        st.error(f"error creando vistas: {e}")
        return False

def cargar_logo():
    """
    carga el logo de la ucv desde diferentes rutas posibles
    returns:
        image: imagen del logo o none si no se encuentra
    """
    try:
        rutas = ["Logo-Ucv.png", "logos/Logo-Ucv.png", "./Logo-Ucv.png"]
        for ruta in rutas:
            if os.path.exists(ruta):
                return Image.open(ruta)
        return None
    except Exception:
        return None
