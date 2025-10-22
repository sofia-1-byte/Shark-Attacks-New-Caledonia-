
import pandas as pd
import plotly.express as px
import streamlit as st
import utils




#Título
st.set_page_config(
    page_title="Gráficos",
    page_icon="",
    layout="wide")

#Varibles del fronT_end
column = ["Año","Tipo de Actividad", "Fatalidad", "Temporada", "Sexo", "Especie de Tiburón", "AM,PM"]
column2 = [x for x in column if x != "Año" ]
df = utils.load_and_clean_data()



#Título
st.markdown('<h1 style="color:#4991f5;text-align:center;">Visual</h1>', unsafe_allow_html=True)
st.markdown("---")

#Botones para pedir al usuario que gráfico quiere ver
kind_graph = st.selectbox("Ingrese el tipo de gráfico que quiere ver", ["Histogramas", "Pie"])



#condicionales segun los graficos
if kind_graph == "Pie":
    check = st.checkbox("Visibilidad de datos")
    if check:
        #Select box para el tipo de variable
        left, right = st.columns(2)
        columna = right.selectbox("Ingrese una Varible Para su Gráfico",
        column2)
        col = utils.formato(columna)
        right.header("Visualización de Tablas")
        right.write(df)
        left.header("Gráfico")
        left.write(utils.grafico_pie(col, True))
    else:
        columna = right.selectbox("Ingrese una Varible Para su Gráfico",
                                  column2)
        left.write(utils.grafico_pie(col, True))
        
if kind_graph == "Histogramas":
    check = st.checkbox("Visibilidad de datos")

    if check:

        #Creamos los espacios visuales
        left, right = st.columns(2)
        columna = left.selectbox("Ingrese una Varible Para su Gráfico", column)
        columna2 = right.selectbox("Ingrese una variable para su grafico", column)
        col = utils.formato(columna)
        col2 = utils.formato(columna2)
        right.header("Visualización de Tablas")
        left.header("Gráfico")
        left.write(utils.grafico_barras(col, True))
        ##Creación de variables para los graficos
        tabla = utils.crear_tablas_doble_entrada(_df= df, fila=col, columna=col2)
        tabla2 = utils.tabla_bivariante(df,col, col2, unk = True)
        ##

        le, ri = right.columns(2)
        key = ri.button("Visual 2")
        key2 = le.button("Visual 1")
        if key:
            right.write(tabla["absoluta"])
        else:
            right.write(tabla2)
    else:
        left, right = st.columns(2)
        columna = left.selectbox("Ingrese una Varible Para su Gráfico", column)
        columna2 = right.selectbox("Ingrese una variable para su grafico", column)
        col = utils.formato(columna)
        col2 = utils.formato(columna2)
        st.header("Gráfico")
        st.write(utils.grafico_barras(col, True))



