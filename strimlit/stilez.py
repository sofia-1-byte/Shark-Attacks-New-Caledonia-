import streamlit as st
import os
from PIL import Image

def cargar_logo(nombre_logo):
    """
    Carga una imagen de logo desde el directorio 'logo' dentro del proyecto.
    
    Args:
        nombre_logo (str): Nombre del archivo de imagen del logo (incluyendo extensión)
        
    Returns:
        Image.Image or None: Objeto de imagen PIL si el logo existe y se puede cargar,
        None si el archivo no existe o hay error en la carga.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(current_dir, "logo", nombre_logo)
        if os.path.exists(ruta_logo):
            return Image.open(ruta_logo)
        return None
    except Exception as e:
        return None

def mostrar_logos():
    """
    Muestra los logos institucionales alineados en los extremos superiores de la interfaz.
    
    Los logos cargados son:
    - UCV.png: Logo de la Universidad Central de Venezuela (lado izquierdo)
    - EECA.png: Logo de la Escuela de Estadística y Ciencias Actuariales (lado derecho)
    """
    logo_ucv = cargar_logo("UCV.png") 
    logo_eeca = cargar_logo("EECA.png")  

    # Crear tres columnas: izquierda, centro y derecha
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if logo_ucv:
            st.image(logo_ucv, width=150)

    with col3:
        if logo_eeca:
            st.image(logo_eeca, width=200)

    st.markdown("---")

def aplicar_estilos_globales():
    """
    Aplica estilos CSS globales para toda la aplicación Streamlit con escala gradual de tamaños.
    
    Define y aplica una hoja de estilos completa que establece:
    - Escala tipográfica para títulos y subtítulos (h1, h2, h3, h4)
    - Colores en tonos azules para títulos
    - Tamaño de fuente aumentado 
    - Mejoras de espaciado, márgenes 
    - Mejores líneas divisorias y listas
    
    """
    st.markdown("""
    <style>
        
        /* Título principal */
        h1 {
            color: #0066CC !important;
            font-size: 52px !important;
            text-align: center !important;
            margin-bottom: 35px !important;
            font-weight: 800 !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1) !important;
        }
        
        /* Primer nivel de subtítulo */
        h2 {
            color: #0052A3 !important;
            font-size: 38px !important;
            border-bottom: 2px solid #B3D9FF !important;
            padding-bottom: 12px !important;
            margin-top: 35px !important;
            margin-bottom: 25px !important;
            font-weight: 700 !important;
        }
        
        /* Segundo nivel de subtítulo */
        h3 {
            color: #003D7A !important;
            font-size: 30px !important;
            margin-top: 30px !important;
            margin-bottom: 20px !important;
            font-weight: 600 !important;
            border-left: 4px solid #0066CC !important;
            padding-left: 15px !important;
        }
        
        /* Tercer nivel de subtítulo */
        h4 {
            color: #002950 !important;
            font-size: 24px !important;
            margin-top: 25px !important;
            margin-bottom: 15px !important;
            font-weight: 600 !important;
        
        }
        
        /* Texto normal  */
        .stMarkdown {
            font-size: 20px !important;
        }
        
        .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol {
            font-size: 20px !important;
            line-height: 1.7 !important;
        }
        
        /* Mejorar el divisor de Streamlit */
        hr {
            border: none !important;
            height: 3px !important;
            background: linear-gradient(90deg, transparent, #0066CC, transparent) !important;
            margin: 30px 0 !important;
        }
        
        /* Estilo para listas */
        .stMarkdown ul, .stMarkdown ol {
            margin-left: 20px !important;
        }
        
        .stMarkdown li {
            margin-bottom: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def aplicar_estilos_tablas():
    """
    Aplica estilos CSS específicos para tablas de datos en la aplicación Streamlit.
    
    Diseña tablas profesionales y consistentes con el resto de la interfaz, incluyendo:
    - Tamaño de fuente igual al contenido general 
    - Encabezados con fondo azul y texto blanco para mejor contraste y jerarquía
    - Filas alternas con colores suaves para mejorar la legibilidad de datos tabulares
    - Efectos hover sutiles para mejorar la interactividad
    - Bordes redondeados y sombreados
    
    """
    st.markdown("""
    <style>
        /* Tablas con el mismo tamaño de texto que el contenido */
        .stDataFrame {
            font-size: 20px !important;
        }
        
        .dataframe {
            font-size: 20px !important;
        }
        
        /* Encabezados de tabla con fondo azul */
        .stDataFrame thead tr th {
            background-color: #1E88E5 !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 20px !important;
            padding: 15px 12px !important;
        }
        
        /* Celdas de tabla */
        .stDataFrame tbody tr td {
            font-size: 20px !important;
            padding: 12px 10px !important;
            border-bottom: 1px solid #E0E0E0 !important;
        }
        
        /* Filas alternas */
        .stDataFrame tbody tr:nth-child(even) {
            background-color: #F8F9FA !important;
        }
        
        /* Efecto hover sutil */
        .stDataFrame tbody tr:hover {
            background-color: #E3F2FD !important;
        }
        
    </style>
    """, unsafe_allow_html=True)