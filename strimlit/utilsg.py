import utils
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import os
from scipy import stats
from PIL import Image

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
def load_and_clean_data1() -> pd.DataFrame:
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
            a.year,
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

        df.loc[df['species'].isin(UNKNOWN_VALUES), 'species'] = 'Desconocido'
        df.loc[df['species'].isna(), 'species'] = 'Desconocido'

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

def grafico_pie(columna: str, excluir: bool = False) :
    """ Genera un gráfico de pie según las proporciones de las columnas de la
    Parameters:
        columna (str): columna de tablas
        excluir (bool, optional): decidir si se excluyen valores desconocidos

    """

    ##Cargar el dataframe.

    df = load_and_clean_data1()

    ##Analizar frecuencias de los fatales
    df_grafico = utils.analizar_frecuencias(df, columna, excluir)
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

#Cambiar el formato del string columna para que sea legible por la funcion de graficos de pie
def formato(columna):
    """Formatea la entrada del back end de las
    variables de la selección en variables que la funcion de gráfico
    de pie pueda leer"""

    if columna == "Tipo de Actividad":
        columna = "activity"
        return columna
    elif columna == "Fatalidad":
        columna = "is_fatal_cat"
        return columna
    elif columna == "Temporada":
        columna = "season"
        return columna
    elif columna == "Sexo":
        columna = "sex"
        return columna
    elif columna == "Especie de Tiburón":
        columna = "species"
        return columna
    elif columna == "AM,PM":
        columna = "day_part"
        return columna
    elif columna == "Década":
        columna = "decada"
        return columna
    elif columna == "Año":
        columna = "year"
        return columna
    else:
        pass

###Gráfico de barras
def grafico_barras(columna: str, columna2: Optional[str] = None, excluir: bool = False):
    """ Genera un gráfico de barras según las proporciones de las columnas elegidas
    Parameters:
        columna (str): columna de tablas
        excluir (bool, optional): decidir si se excluyen valores desconocidos
        bi: gráfico de barras bivariante

    """
    ##Cargar base de datos
    df = load_and_clean_data1()

    if columna2 != None:


        ##Analizar frecuencias de los fatales

        frecuencia = tabla_bivariante(df, columna, columna2, excluir)
        frecuencia2 = utils.analizar_frecuencias(df, columna, excluir)

        ##Condicionar titulos para el gráfico de pie según las variables
        if columna == "activity":
            title = "Proporcion de ataques según actividad"
        elif columna == "is_fatal_cat":
            title = "Proporción de ataques según fatalidad"
        elif columna == "year":
            title = "Cantidad de ataques según el año"
        elif columna == "season":
            title = "Proporción de ataques según Temporada"
        elif columna == "sex":
            title = "Proporción de ataques según sexo de las víctimas"
        elif columna == "species":
            title = "Proporción de ataques según la Especie de Tiburón"
        elif columna == "day_part":
            title = "Proporción de ataques según el horario"

        ## Construcción del gráfico
        if columna2 == None:
            fig = px.bar(frecuencia2, x=columna, y='count', title=title)
            return fig

        else:
            fig = px.bar(frecuencia, x=columna, y='count', color=columna2, title=title)
            return fig
    else:
        frecuencia = utils.analizar_frecuencias(df, columna, excluir)

        ##Condicionar titulos para el gráfico de pie según las variables
        if columna == "activity":
            title = "Proporcion de ataques según actividad"
        elif columna == "is_fatal_cat":
            title = "Proporción de ataques según fatalidad"
        elif columna == "year":
            title = "Cantidad de ataques según el año"
        elif columna == "season":
            title = "Proporción de ataques según Temporada"
        elif columna == "sex":
            title = "Proporción de ataques según sexo de las víctimas"
        elif columna == "species":
            title = "Proporción de ataques según la Especie de Tiburón"
        elif columna == "day_part":
            title = "Proporción de ataques según el horario"

        ## Construcción del gráfico
        fig = px.bar(frecuencia, x='Categoria', y='Frecuencia Absoluta', title=title)
        return fig

def grafico_caja(_df,columna):
    """
    Permite hacer un gráfico de cága según alguna varibale cualquiera
    """

    a = utils.analizar_frecuencias(_df, columna)
    fig = px.box(a, x="Frecuencia Absoluta", y="Categoria")

    return fig


###Tabla bivariante vertical
def tabla_bivariante(_df: pd.DataFrame, species: str, is_fatal_cat: str, unk: bool):
    """Crea una tabla bivariante vertical que permite hacer gráficos de barras agrupados
    Parámetros:
    _df: dataframe
    species: variable 1
    is_fatal_cat: variable 2
    unk: True = Descartar valores "Desconocidos"
    """

    if unk:
        df = _df[(_df[species] != "Desconocido") & (_df[is_fatal_cat] != "Desconocido")].copy()
    else:
        df = _df

    a = df[species].value_counts()
    list = a.index
    # lista de la segunda varible
    c = df[is_fatal_cat].value_counts()
    list2 = c.index

    # Nuevo DataFrame

    # lista de dataframe
    df_list = []
    df.columns
    # Revisa cada fila
    for x in list:
        # Revisa una columna por cada fila
        for y in list2:
            # filtramos
            b = df.loc[(df[species] == x) & (df[is_fatal_cat] == y), species].value_counts()
            # revisamos si es el inicio del programa (primera celda)
            if y == list2[0] and x == list[0]:

                if not b.empty:
                    b1 = b.index
                    b2 = b.values
                    data = pd.DataFrame({
                        species: [b1[0]]})
                    data2 = pd.DataFrame({
                        is_fatal_cat: [y]})
                    data3 = pd.DataFrame({
                        "count": [b2[0]]})
                    data = pd.concat([data, data2, data3], axis=1)

                else:
                    data = pd.DataFrame({
                        species: [x]})
                    data2 = pd.DataFrame({
                        is_fatal_cat: [y]})
                    data3 = pd.DataFrame({
                        "count": [0]})
                    data = pd.concat([data, data2, data3], axis=1)


            else:
                if not b.empty:
                    b1 = b.index
                    b2 = b.values
                    data1 = pd.DataFrame({
                        species: [b1[0]]})
                    data2 = pd.DataFrame({
                        is_fatal_cat: [y]})
                    data3 = pd.DataFrame({
                        "count": [b2[0]]})
                    data4 = pd.concat([data1, data2, data3], axis=1)

                    data = pd.concat([data4, data], axis=0)
                else:
                    data1 = pd.DataFrame({
                        species: [x]})
                    data2 = pd.DataFrame({
                        is_fatal_cat: [y]})
                    data3 = pd.DataFrame({
                        "count": [0]})
                    data4 = pd.concat([data1, data2, data3], axis=1)

                    data = pd.concat([data4, data], axis=0)

    return data




