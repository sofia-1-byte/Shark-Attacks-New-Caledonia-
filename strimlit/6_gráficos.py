import pandas as pd
import plotly.express as px
import streamlit as st
import utils 

#Título
st.write("""Graficos""")

#Varibles del fronend
column = ["Tipo de Actividad", "Fatalidad", "Temporada", "Sexo", "Especie de Tiburón", "AM,PM"]

df = utils.load_and_clean_data()

#Select box para el tipo de variable
columna = st.selectbox("Ingrese una Varible Para su Gráfico",
   column)

#Cambiar el formato del string columna para que sea legible por la funcion de graficos de pie
if columna == "Tipo de Actividad":
    columna = "activity"
elif columna == "Fatalidad":
    columna = "is_fatal_cat"
elif columna == "Temporada":
    columna = "season"
elif columna == "Sexo":
    columna = "sex"
elif columna == "Especie de Tiburón":
    columna = "species"
elif columna == "AM,PM":
    columna = "day_part"


st.write(df)
st.write(utils.grafico_pie(columna, True))



