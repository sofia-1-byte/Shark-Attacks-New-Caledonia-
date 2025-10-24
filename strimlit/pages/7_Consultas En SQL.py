import streamlit as st
import pandas as pd
import os
import stilez 
import utilsql 

st.set_page_config(
    page_title="Consultas SQL - Ataques de tiburón",
    page_icon="🦈",
    layout="wide"
)

# Crear columnas 
col1, col2 = st.columns([3, 1])

stilez.aplicar_estilos_globales()

# titulo principal
st.title("Consultas SQL")
st.markdown("---")

# consulta 1: ataques por estacion del año
codigo1 = """
SELECT 
    season as estacion,
    COUNT(*) as cantidad_ataques,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shark_attackdatos 
    WHERE season IS NOT NULL AND season != 'Desconocido')), 2) as porcentaje
FROM shark_attackdatos 
WHERE season IS NOT NULL AND season != 'Desconocido'
GROUP BY season
ORDER BY cantidad_ataques DESC;
"""

utilsql.mostrar_consulta(
    utilsql.obtener_ataques_por_estacion,
    "1. Ataques de tiburón por estación del año",
    "Muestra cuantos ataques de tiburones ocurrieron en cada estación del año, ordenados de mayor a menor frecuencia.",
    codigo1
)

# consulta 2: top 5 actividades fatales
codigo2 = """
SELECT 
    activity as actividad,
    COUNT(*) as ataques_fatales
FROM shark_attackdatos 
WHERE is_fatal = 'Y' 
    AND activity IS NOT NULL 
    AND activity != 'Desconocido'
GROUP BY activity
ORDER BY ataques_fatales DESC
LIMIT 5;
"""

utilsql.mostrar_consulta(
    utilsql.obtener_top5_actividades_fatales,
    "2. Top 5 actividades con más ataques fatales",
    "Determina el número de ataques fatales según la actividad realizada, mostrando solo las cinco actividades con más ataques fatales.",
    codigo2
)

# consulta 3: ataques por fase lunar
codigo3 = """
SELECT 
    moon_phase as fase_lunar,
    COUNT(*) as cantidad_ataques,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shark_attackdatos 
    WHERE moon_phase IS NOT NULL AND moon_phase != 'Desconocido')), 2) as porcentaje
FROM shark_attackdatos 
WHERE moon_phase IS NOT NULL AND moon_phase != 'Desconocido'
GROUP BY moon_phase
ORDER BY cantidad_ataques DESC;
"""

utilsql.mostrar_consulta(
    utilsql.obtener_ataques_por_fase_lunar,
    "3. Ataques por fase lunar",
    "Relaciona la fase lunar con la cantidad de ataques ocurridos bajo cada una, mostrando el porcentaje respecto al total.",
    codigo3
)

codigo4 = """
SELECT DISTINCT
    a.species as especie,
    s.conservation_status as categoria_conservacion,
    cs.cat as descripcion_completa
FROM shark_attackdatos a
INNER JOIN SHARKS s ON a.species = s.id
INNER JOIN conservation_status cs ON s.conservation_status = cs.id_long
WHERE a.species IS NOT NULL 
    AND a.species != 'Desconocido'
    AND a.species != '';
"""

utilsql.mostrar_consulta(
    utilsql.obtener_especies_conservacion,
    "4. Especies implicadas con categoria de conservacion",
    "Enlista las especies implicadas en ataques junto con su categoria de conservación y descripción mostrando solo una fila por especie.",
    codigo4
)

# consulta 5: ataques fatales por decada
codigo5 = """
SELECT 
    CASE 
        WHEN year BETWEEN 1900 AND 1909 THEN '1900-1909'
        WHEN year BETWEEN 1910 AND 1919 THEN '1910-1919'
        WHEN year BETWEEN 1920 AND 1929 THEN '1920-1929'
        WHEN year BETWEEN 1930 AND 1939 THEN '1930-1939'
        WHEN year BETWEEN 1940 AND 1949 THEN '1940-1949'
        WHEN year BETWEEN 1950 AND 1959 THEN '1950-1959'
        WHEN year BETWEEN 1960 AND 1969 THEN '1960-1969'
        WHEN year BETWEEN 1970 AND 1979 THEN '1970-1979'
        WHEN year BETWEEN 1980 AND 1989 THEN '1980-1989'
        WHEN year BETWEEN 1990 AND 1999 THEN '1990-1999'
        WHEN year BETWEEN 2000 AND 2009 THEN '2000-2009'
        WHEN year BETWEEN 2010 AND 2019 THEN '2010-2019'
        WHEN year BETWEEN 2020 AND 2025 THEN '2020-2025'
        ELSE 'Otra'
    END as decada,
    COUNT(*) as ataques_fatales
FROM shark_attackdatos 
WHERE is_fatal = 'Y' 
    AND year IS NOT NULL
GROUP BY decada
ORDER BY MIN(year);
"""

utilsql.mostrar_consulta(
    utilsql.obtener_ataques_fatales_por_decada,
    "5. Ataques fatales por decada",
    "Cuenta el número de ataques fatales por década, usando la columna year. Crea una nueva columna llamada década que agrupe los años desde 1900 hasta 2025.",
    codigo5
)

# resumen 
st.markdown("### Resumen")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total consultas ejecutadas", 
        "5",
        "Consultas SQL completadas"
    )

with col2:
    # obtener datos para metricas
    df_estaciones = utilsql.obtener_ataques_por_estacion()
    total_estaciones = len(df_estaciones) if not df_estaciones.empty else 0
    st.metric(
        "Estaciones analizadas", 
        total_estaciones,
        "Distribución temporal"
    )

with col3:
    df_especies = utilsql.obtener_especies_conservacion()
    total_especies = len(df_especies) if not df_especies.empty else 0
    st.metric(
        "Especies identificadas", 
        total_especies,
        "En ataques"
    )


st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Consultas SQL")
