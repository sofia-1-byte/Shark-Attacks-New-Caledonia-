import pandas as pd
import plotly.express as px
import streamlit as st
import utils
import utilsg
import stilez 

st.set_page_config(
    page_title="Graficos, Visuales e Interpretación de los datos 📊",
    page_icon="🦈",
    layout="wide")

#Varibles del fronT_end
especial = ["AM,PM"]

column = ["Año","Tipo de Actividad", "Fatalidad", "Temporada", "Sexo", "Especie de Tiburón",  "País"]
column2 = [x for x in column if (x != "Año")  ]
df = utilsg.load_and_clean_data1()

stilez.aplicar_estilos_globales()

# titulo principal
st.title("Visuales e Interpretación 📊")

##Realizamos una página por definición y otra personalizable
tab1, tab2 = st.tabs([
    "Análisis", "Personalizar"
])

with tab1:
    st.header("1. Fatalidad 💀")


    st.plotly_chart(utilsg.grafico_pie("is_fatal_cat", True), key = "1")

    st.write(
        "**Descripción:** Se puede notar que la mayoría de los ataques registrados son fatales, específicamente un 78% del total de ataques"
        " registrados, mientras que el total de ataques no fatales registrados corresponden a un 22%")


    st.header("2. Actividad 🌊")




    tab3, tab4 =st.tabs(["Normal", "Detallado"])
    with tab3:
        st.plotly_chart(utilsg.grafico_barras("activity", columna2=None, excluir=True), key = "2")
        st.markdown(
            "**Descripción**: En este gráfico se puede ver la cantidad de de ataques según la actividad que realizaba la victima."
            " Las actividades que mas han presentado víctimas son: surfear (21.38%), bodybooarding (19,52%), pescar (19.48%), nadar (17.28%) y "
            " paddle boarding (7.28%). En total estás cinco actividades mayormente reportadas en los ataques suponen un 84.94 %"
            " de los ataques totales. Con esto podría pensarse que el resto de actividades son menos frecuentes en los registros de "
            " ataques de tiburones por ser menos"
            " pupulares en las zonas donde ocurren ataques, o incluso, menos populares en general ")

    with tab4:
        st.plotly_chart(utilsg.grafico_barras("activity", "is_fatal_cat", excluir=True), key="4")

        st.markdown("**Descripción:** Pueden verse la cantidad de de ataques según la actividad que realizaba la víctima"
                " además verificando si fue o no fatal el ataque registrado: Aquí se puede ver que la mayoría de ataques fatales"
                    " fueron victimas que se encontraban nadando (6.48%). De segundo lugar se encuentra el BodyBoarding con un (6.27%),"
                    " esto podría sugerir que el hecho de tener el cuerpo mas cercano al agua implica mayor riesgo de un ataque fatal,"
                    " o incluso que la forma en la que se mueve la víctima la haga suceptible de ser atacada por un tiburón . De tercer"
                    " lugar está la Pesca (3.28%), de cuarto el Paddle Bording (2%) y por ultimo el surfeo (1.4%)")

    ####
    st.header("3. Paises más Atacados 🏴 ")
    bars = st.slider("Número de países en el gráfico", 0, 105, 10)

    fig = utilsg.grafico_barras_paises(columna="country", columna2=None, number=bars, excluir=True)
    st.plotly_chart(fig, key="3")

    st.markdown(f"**Descripción:** Puede verse el porcentaje de ataques según el top **{bars}** de países con"
                " más ataques. Los países con mas ataques reportados son: Estados Unidos(38.73%), Australia (20.92%), Sudafrica (10.32%),"
                " Nueva Guinea (2.2%) y Nueva Caledonia (2.12%). Entre los 5 países con más reportes"
                " se encuentra el 74.29% del total de todos los ataques registrados.")
    #####


    st.header("4. Distribución de las Edades ⚠️ ")

    st.markdown("**Edad y Frecuencia**")

    hist = utilsg.histograma_edad(columna=None, valor=None, number= 20)
    st.plotly_chart(hist, key="87")

    st.markdown("**Descripción**: En este gráfico se puede visualizar que la distribucion de las edades tiene"
                " una forma leptocurtica con un sesgo positivo, Además se observa que la mayoría"
                " de edades se encuentran entre 20 y 24 años. Podemos concluir entonces que"
                " la mayoría de personas que han sido atacadas son en su mayoría jovenes o adultos"
                " jóvenes.")


    st.header("5. Cantidad de Ataques Segun Temporada 🍃")

    lab1, lab2 = st.tabs(["Temporada", "Temporada y Fatalidad"])

    with lab1:
        st.plotly_chart(utilsg.grafico_pie("season", True), key="9")

        st.markdown(f"**Descripción:** Se observan los porcentajes de"
                    " los ataques según las estaciones del año. Como se puede ver en el gráfico,"
                    " las proporciones de los ataques según la época del año son muy parecidas entre si, "
                    " no existe mucha diferencia,"
                    " Sin embargo es resaltable que la mayoría de"
                    " ataques de tiburón suceden en el invierno (29.3%).")
    with lab2:
        hola = utilsg.grafico_barras("season", "is_fatal_cat", excluir=True)
        st.plotly_chart(hola, key="1001")
        st.markdown(f"**Descripción:** Se observan los porcentajes de"
                    " los ataques según las estaciones del año y su fatalidad. Se puede ver en el gráfico que"
                    " las proporciones de los ataques no fatales en su mayoría suceden en el invierno (23.76)"
                    ". Así mismo se puede"
                    " observar que la mayoría de ataques fatales ocurrieron durante el verano (6.12%), cuando las personas"
                    " son más activas en las costas.")










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
            columna = right.selectbox("Variable",
                                      column2)
            col = utilsg.formato(columna)
            right.header("Tablas")
            ##
            tab = utils.analizar_frecuencias(df, col)
            right.write(tab)
            left.header("Visual")
            left.write(utilsg.grafico_pie(col, True))
        else:
            columna = st.selectbox("Variable",
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

                columna = left.selectbox("Variable 1", column2)

                column1 = [x for x in column2 if x != columna]

                columna2 = right.selectbox("Variable 2", column1)
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
                columna = left.selectbox("Variable 1", column2)

                column1 = [x for x in column2 if x != columna]

                columna2 = right.selectbox("Variable 2", column1)
                col = utilsg.formato(columna)
                col2 = utilsg.formato(columna2)
                st.header("Visual")
                st.write(utilsg.grafico_barras(col, col2, True))
        else:
            if check:

                # Creamos los espacios visuales
                left, right = st.columns(2)

                ##variables de loss
                columna = left.selectbox("Variable", column)

                col = utilsg.formato(columna)

                right.header("Tablas")
                left.header("Visual")
                left.write(utilsg.grafico_barras(col, columna2=None, excluir=True))
                ##Creación de variables para los graficos
                tabla = utils.analizar_frecuencias(df, col)
                right.write(tabla)

            else:
                left, right = st.columns(2)
                columna = left.selectbox("Variable", column)

                col = utilsg.formato(columna)

                st.header("Visual")
                st.write(utilsg.grafico_barras(col, columna2=None, excluir=True))

    if kind_graph == "Caja y Bigote":
        left, right = st.columns(2)

        columna = left.selectbox("Variable", column2)
        left.header(f"Visual según edad y {columna}")
        col = utilsg.formato(columna)
        st.write(utilsg.grafico_caja(df, col))




