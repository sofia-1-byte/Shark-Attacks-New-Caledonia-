import pandas as pd
import plotly.express as px
import streamlit as st
import utils
import utilsg

st.set_page_config(
    page_title="Gráficos",
    page_icon="🦈",
    layout="wide")

#Varibles del fronT_end
column = ["Año","Tipo de Actividad", "Fatalidad", "Temporada", "Sexo", "Especie de Tiburón", "AM,PM"]
column2 = [x for x in column if x != "Año" ]
df = utilsg.load_and_clean_data1()





# titulo principal
st.title("Gráficos")
st.markdown("---")

tab1, tab2 = st.tabs([
    "Análisis", "Personalizar"
])

with tab1:
    st.write("aquí no hay un coño xd")

with tab2:
    # Botones para pedir al usuario que gráfico quiere ver
    kind_graph = st.selectbox("Ingrese el tipo de gráfico que quiere ver", ["Histogramas", "Pie", "Caja y Bigote"])

    # condicionales segun los graficos
    if kind_graph == "Pie":
        check = st.checkbox("Visibilidad de datos")
        if check:
            # Select box para el tipo de variable
            left, right = st.columns(2)
            columna = right.selectbox("Ingrese una Varible Para su Gráfico",
                                      column2)
            col = utilsg.formato(columna)
            right.header("Tablas")
            ##
            tab = utils.analizar_frecuencias(df, col)
            right.write(tab)
            left.header("Visual")
            left.write(utilsg.grafico_pie(col, True))
        else:
            columna = st.selectbox("Ingrese una Varible Para su Gráfico",
                                   column2)
            st.header("Visual")
            col = utilsg.formato(columna)
            st.write(utilsg.grafico_pie(col, True))

    if kind_graph == "Histogramas":
        check = st.checkbox("Visibilidad de datos")
        check2 = st.checkbox("Bivariante")
        if check2:

            if check:

                # Creamos los espacios visuales
                left, right = st.columns(2)

                columna = left.selectbox("Ingrese una Varible Para su Gráfico", column2)

                column1 = [x for x in column2 if x != columna]

                columna2 = right.selectbox("Ingrese una variable para su grafico", column1)
                col = utilsg.formato(columna)
                col2 = utilsg.formato(columna2)
                right.header("Tablas")
                left.header("Visual")
                left.write(utilsg.grafico_barras(col, col2, True))
                ##Creación de variables para los graficos
                tabla = utils.crear_tablas_doble_entrada(_df=df, fila=col, columna=col2)
                tabla2 = utilsg.tabla_bivariante(df, col, col2, unk=True)
                ##

                le, ri = right.columns(2)
                key = ri.button("Vertical ")
                key2 = le.button("Contingencia")
                if key:
                    right.write(tabla2)
                else:

                    right.write(tabla["absoluta"])
            else:
                left, right = st.columns(2)

                ### Remover los años cua
                columna = left.selectbox("Ingrese una Varible Para su Gráfico", column2)

                column1 = [x for x in column2 if x != columna]

                columna2 = right.selectbox("Ingrese una variable para su grafico", column1)
                col = utilsg.formato(columna)
                col2 = utilsg.formato(columna2)
                st.header("Visual")
                st.write(utilsg.grafico_barras(col, col2, True))
        else:
            if check:

                # Creamos los espacios visuales
                left, right = st.columns(2)

                ##variables de loss
                columna = left.selectbox("Ingrese una Varible Para su Gráfico", column)

                col = utilsg.formato(columna)

                right.header("Tablas")
                left.header("Visual")
                left.write(utilsg.grafico_barras(col, columna2=None, excluir=True))
                ##Creación de variables para los graficos
                tabla = utils.analizar_frecuencias(df, col)
                right.write(tabla)

            else:
                left, right = st.columns(2)
                columna = left.selectbox("Ingrese una Varible Para su Gráfico", column)

                col = utilsg.formato(columna)

                st.header("Visual")
                st.write(utilsg.grafico_barras(col, columna2=None, excluir=True))

    if kind_graph == "Caja y Bigote":
        left, right = st.columns(2)

        columna = left.selectbox("Ingrese una Varible Para su Gráfico", column2)
        left.header(f"Visual según edad y {columna}")
        col = utilsg.formato(columna)
        st.write(utilsg.grafico_caja(df, col))




