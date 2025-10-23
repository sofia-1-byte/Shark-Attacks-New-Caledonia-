import streamlit as st

def aplicar_estilos_globales():
    """
    Aplica estilos bonitos a al texto y títulos de la app
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