import streamlit as st
import utils

st.set_page_config(
    page_title="Introducción - Ataques de Tiburón",
    page_icon="",
    layout="wide"
)

# mostrar header con logos
utils.mostrar_header()

# Título principal centrado
st.markdown('<h1 style="color:#4991f5;text-align:center;">Introducción</h1>', unsafe_allow_html=True)

st.markdown("---")

# contenido principal
st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
## texto de la introducción

</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Introducción")