import pandas as pd
import plotly.express as px
import streamlit as st
import utils
import utilsg
import stilez 

st.set_page_config(
    page_title="Gráficos 📊",
    page_icon="🦈",
    layout="wide")

#Varibles del fronT_end
column = ["Año","Tipo de Actividad", "Fatalidad", "Temporada", "Sexo", "Especie de Tiburón", "AM,PM", "País"]
column2 = [x for x in column if (x != "Año")  ]
df = utilsg.load_and_clean_data1()

stilez.aplicar_estilos_globales()

# titulo principal
st.title("Gráficos 📊")

##Realizamos una página por definición y otra personalizable
tab1, tab2 = st.tabs([
    "Análisis", "Personalizar"
])

with tab1:
    st.header("1. Fatalidad 💀")
    st.markdown("**Proporción de ataques fatales y no fatales**")

    st.plotly_chart(utilsg.grafico_pie("is_fatal_cat", True), key = "1")
    st.write("**Descripción:**: La mayoría de los ataques registrados son fatales, específicamente un 78% del total de ataques"
             " registrados")

    st.header("2. Actividad 🌊")
    st.markdown("**Descripción: Evaluación del riesgo de ataques según el tipo de actividad que realizaba la victima**")


    tab3, tab4 =st.tabs(["Normal", "Detallado"])
    with tab3:
        st.plotly_chart(utilsg.grafico_barras("activity", columna2=None, excluir=True), key = "2")

        st.markdown("Descripción: En este gráfico pueden verse la cantidad de de ataques según la actividad que realizaba la victima."
                    " Las actividades que mas han presentado víctimas son: surfear, bodybooarding, pescar, nadar y "
                    "paddle boarding ")

    with tab4:
        st.plotly_chart(utilsg.grafico_barras("activity", "is_fatal_cat", excluir=True), key="4")

        st.markdown("**Descripción:** Pueden verse la cantidad de de ataques según la actividad que realizaba la victima"
                " además verificando si fue o no fatal el ataque registrado")

    st.header("3. Paises más Atacados ⚠️ ")
    bars = st.slider("Número de países en el gráfico", 0, 105, 10)

    fig= utilsg.grafico_barras_paises(columna =  "country", columna2=None, number = bars,  excluir=True)
    st.plotly_chart(fig, key="3")

    st.markdown(f"**Descripción:** Pueden verse el porcentaje de ataques según el top **{bars}** de países con"
                " más ataques")

    st.header("4. Distribución de las Edades segun fatal y no fatal ⚠️ ")

    tab5, tab6 = st.tabs(["Distribución", "Distribución Detallada"])
    with tab5:

        bars1 = st.slider("número de barras del histograma", 0, 20, 7)
        hist = utilsg.histograma_edad(columna=None, valor=None, number=bars1)
        st.plotly_chart(hist, key="5")

    with tab6:
        left, right = st.columns(2)



##Personalizar gráficos
with tab2:
    # Botones para pedir al usuario que gráfico quiere ver
    kind_graph = st.selectbox("Ingrese el tipo de gráfico que quiere ver", ["Histograma", "Pie", "Caja y Bigote"])

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

    if kind_graph == "Histograma":
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




