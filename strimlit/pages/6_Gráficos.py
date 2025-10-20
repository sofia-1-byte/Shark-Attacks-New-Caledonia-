
import pandas as pd
import plotly.express as px
import streamlit as st
import utils
#Varibles del fronend
column = ["Año","Tipo de Actividad", "Fatalidad", "Temporada", "Sexo", "Especie de Tiburón", "AM,PM"]
df = utils.load_and_clean_data()

#Título
st.set_page_config(
    page_title="Gráficos",
    page_icon="",
    layout="wide")

#Título
st.markdown('<h1 style="color:#4991f5;text-align:center;">Gráficos</h1>', unsafe_allow_html=True)
st.markdown("---")

#Botones para pedir al usuario que gráfico quiere ver
kind_graph = st.selectbox("Ingrese el tipo de gráfico que quiere ver", ["Histogramas", "Pie"])

if kind_graph == "Pie":
    #Select box para el tipo de variable
    columna = st.selectbox("Ingrese una Varible Para su Gráfico",
    column)
#Formateamos la entrada de la selectbox
    col = utils.formato(columna)

    st.write(df)
    st.write(utils.grafico_pie(col, True))
elif kind_graph == "Histogramas":

    columna = st.selectbox("Ingrese una Varible Para su Gráfico", column)

    col = utils.formato(columna)
    st.write(utils.grafico_barras(col, True))


