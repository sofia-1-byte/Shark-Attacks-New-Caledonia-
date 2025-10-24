import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional
import utils

COLORES = {
    'fatal': '#1f77b4',      
    'no_fatal': '#aec7e8',     
    'principal': '#2E86AB',    
    'edad': '#3498DB',         
    'secundario': '#A3D5F7',   
    'fondo': '#F0F8FF',
    'acento': "#1D6DD4"  
}

# Paletas para gráficos
PALETA_AZULES = ['#1f77b4', '#aec7e8', '#6baed6', '#3182bd', '#08519c', '#d0d1e6', '#9ecae1', '#c6dbef']
PALETA_SECUENCIAL = 'Blues'

def load_and_clean_data1() -> pd.DataFrame:
    """Carga datos usando utils y añade transformaciones específicas para gráficos"""
    df, _ = utils.cargar_datos_y_estadisticas()
    
    # Añadir transformaciones específicas para gráficos
    # Limpieza y categorización de actividades
    df['activity'] = df['activity'].astype(str).str.upper().str.strip()
    
    activity_mapping = {
        'SURFING': 'Surfing', 'SURF': 'Surfing', 'SURFER': 'Surfing',
        'BODYBOARDING': 'Bodyboarding', 'BODY BOARDING': 'Bodyboarding', 'BOOGIE BOARDING': 'Bodyboarding',
        'FISHING': 'Pesca', 'FISHERMAN': 'Pesca', 'SPEARFISHING': 'Pesca',
        'SWIMMING': 'Natación', 'SWIM': 'Natación', 'SWIMMER': 'Natación',
        'PADDLE BOARDING': 'Paddle Boarding', 'STAND-UP PADDLE BOARDING': 'Paddle Boarding',
        'DIVING': 'Buceo', 'SCUBA DIVING': 'Buceo', 'SNORKELING': 'Buceo',
        'WADING': 'Vadeo', 'WADE FISHING': 'Vadeo',
        'KAYAKING': 'Kayaking', 'CANOEING': 'Kayaking',
        'SURF-SKIING': 'Surf-skiing', 'SURF SKIING': 'Surf-skiing',
        'ROWING': 'Remo', 'ROWBOAT': 'Remo'
    }
    
    df['activity_clean'] = df['activity'].map(activity_mapping)
    df.loc[df['activity_clean'].isna(), 'activity_clean'] = 'Otras actividades'
    
    # Limpieza de temporadas
    season_mapping = {
        'WINTER': 'Invierno', 'SUMMER': 'Verano', 
        'SPRING': 'Primavera', 'FALL': 'Otoño', 'AUTUMN': 'Otoño'
    }
    df['season_clean'] = df['season'].map(season_mapping).fillna('Desconocido')
    
    # Crear grupos de edad (igual que en Estadísticas Descriptivas)
    bins = [0, 18, 30, 45, 60, 100]
    labels = ['0-18', '19-30', '31-45', '46-60', '60+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    
    return df

def grafico_fatalidad_interactivo() -> go.Figure:
    """Gráfico circular interactivo para fatalidad usando datos de utils"""
    df = load_and_clean_data1()
    
    # Usar analizar_frecuencias de utils para obtener datos consistentes
    tabla_fatalidad = utils.analizar_frecuencias(df, 'is_fatal_cat', excluir_desconocido=True)
    
    # Filtrar solo datos conocidos de fatalidad
    fatal_data = tabla_fatalidad[tabla_fatalidad['Categoria'].isin(['Fatal', 'No Fatal'])]
    
    # Calcular porcentajes para mostrar en etiquetas
    total = fatal_data['Frecuencia Absoluta'].sum()
    fatal_data = fatal_data.copy()
    fatal_data['Porcentaje'] = (fatal_data['Frecuencia Absoluta'] / total * 100).round(1)
    fatal_data['Etiqueta'] = fatal_data['Categoria'] + '<br>' + fatal_data['Porcentaje'].astype(str) + '%'
    
    fig = go.Figure(data=[
        go.Pie(
            labels=fatal_data['Etiqueta'],
            values=fatal_data['Frecuencia Absoluta'],
            hole=0.4,
            marker=dict(colors=[COLORES['fatal'], COLORES['no_fatal']]),
            textinfo='label',
            hovertemplate='<b>%{label}</b><br>%{value} casos<extra></extra>',
            textposition='inside',
            textfont=dict(size=14)
        )
    ])
    
    fig.update_layout(
        title_text="Distribución de Fatalidad en Ataques de Tiburón",
        showlegend=False,
        annotations=[dict(text=f'Total:<br>{total}', x=0.5, y=0.5, font_size=14, showarrow=False)]
    )
    
    return fig

def grafico_actividad_interactivo(condicionar_fatalidad: bool = False) -> go.Figure:
    """Gráfico de actividades usando tablas de utils"""
    df = load_and_clean_data1()
    
    if condicionar_fatalidad:
        # Usar crear_tablas_doble_entrada de utils para datos consistentes
        tablas = utils.crear_tablas_doble_entrada(df, 'activity_clean', 'is_fatal_cat')
        
        if not tablas:
            return go.Figure()
        
        tabla_absoluta = tablas['absoluta']
        # Quitar totales y tomar top actividades
        tabla_absoluta = tabla_absoluta.drop('Total', axis=0).drop('Total', axis=1)
        top_activities = tabla_absoluta.sum(axis=1).nlargest(8).index
        tabla_absoluta = tabla_absoluta.loc[top_activities]
        
        # Calcular porcentajes para el tooltip
        total_por_actividad = tabla_absoluta.sum(axis=1)
        
        fig = go.Figure()
        
        for fatal_type in ['Fatal', 'No Fatal']:
            if fatal_type in tabla_absoluta.columns:
                color = COLORES['fatal'] if fatal_type == 'Fatal' else COLORES['no_fatal']
                porcentajes = (tabla_absoluta[fatal_type] / total_por_actividad * 100).round(1)
                
                fig.add_trace(go.Bar(
                    name=fatal_type,
                    x=tabla_absoluta.index,
                    y=tabla_absoluta[fatal_type],
                    marker_color=color,
                    text=tabla_absoluta[fatal_type].astype(str) + '<br>(' + porcentajes.astype(str) + '%)',
                    textposition='outside',  # Cambiado a 'outside' para mejor visibilidad
                    hovertemplate=f'<b>%{{x}}</b><br>{fatal_type}: %{{y}} casos<extra></extra>'
                ))
        
        # Calcular el máximo valor para ajustar el margen superior
        max_valor = tabla_absoluta.max().max()
        
        fig.update_layout(
            title="Actividades más Comunes - Condicionado por Fatalidad",
            xaxis_title="Actividad",
            yaxis_title="Número de Ataques",
            barmode='group',
            showlegend=True,
            margin=dict(t=100, b=100),  # Aumentar márgenes superior e inferior
            height=500  # Altura fija para mejor visualización
        )
        
        # Ajustar rango del eje Y para dar espacio a las etiquetas
        fig.update_yaxes(range=[0, max_valor * 1.15])
        
    else:
        # Usar analizar_frecuencias de utils para datos consistentes
        tabla_actividad = utils.analizar_frecuencias(df, 'activity_clean', excluir_desconocido=True)
        top_actividades = tabla_actividad.head(8)
        
        fig = px.bar(
            top_actividades,
            x='Categoria',
            y='Frecuencia Absoluta',
            title="Actividades más Comunes en Ataques de Tiburón",
            labels={'Categoria': 'Actividad', 'Frecuencia Absoluta': 'Número de Ataques'},
            color='Frecuencia Absoluta',
            color_continuous_scale=PALETA_SECUENCIAL,
            text='Frecuencia Relativa %'  # Mostrar porcentajes en barras
        )
        
        fig.update_traces(
            texttemplate='%{y}<br>(%{text}%)',
            textposition='outside'
        )
        
        # Ajustar márgenes y altura
        fig.update_layout(
            margin=dict(t=100, b=100),
            height=500
        )
        
        # Ajustar rango del eje Y
        max_valor = top_actividades['Frecuencia Absoluta'].max()
        fig.update_yaxes(range=[0, max_valor * 1.15])
    
    return fig

def grafico_edad_interactivo(condicionar_fatalidad: bool = False) -> go.Figure:
    """Gráfico de distribución de edad"""
    df = load_and_clean_data1()
    
    # Filtrar edades válidas
    age_data = df[df['age'].notna()]
    
    if condicionar_fatalidad:
        # Filtrar solo Fatal y No Fatal
        age_data = age_data[age_data['is_fatal_cat'].isin(['Fatal', 'No Fatal'])]
        
        fig = px.histogram(
            age_data,
            x='age',
            color='is_fatal_cat',
            nbins=20,
            barmode='overlay',
            opacity=0.7,
            color_discrete_map={'Fatal': COLORES['fatal'], 'No Fatal': COLORES['no_fatal']},
            title="Distribución de Edad - Condicionado por Fatalidad"
        )
        
        fig.update_layout(
            xaxis_title="Edad (años)",
            yaxis_title="Número de Ataques",
            legend_title="Fatalidad",
            margin=dict(t=80, b=80),
            height=450
        )
    else:
        # Usar color VERDE para el gráfico no condicionado
        fig = px.histogram(
            age_data,
            x='age',
            nbins=20,
            title="Distribución de Edad de las Víctimas",
            labels={'age': 'Edad (años)', 'count': 'Número de Ataques'},
            color_discrete_sequence=[COLORES['edad']]  # VERDE para edad no condicionada
        )
        
        # Añadir línea de media usando estadísticas de utils
        mean_age = age_data['age'].mean()
        fig.add_vline(x=mean_age, line_dash="dash", line_color=COLORES['acento'], 
                     annotation_text=f"Media: {mean_age:.1f} años")
        
        fig.update_layout(
            margin=dict(t=80, b=80),
            height=450
        )
    
    return fig

def grafico_grupo_edad_interactivo(condicionar_fatalidad: bool = False) -> go.Figure:
    """Gráfico de grupos de edad usando funciones de utils"""
    df = load_and_clean_data1()
    
    if condicionar_fatalidad:
        # Usar crear_tablas_doble_entrada de utils
        tablas = utils.crear_tablas_doble_entrada(df, 'age_group', 'is_fatal_cat')
        
        if not tablas:
            return go.Figure()
        
        tabla_absoluta = tablas['absoluta']
        tabla_absoluta = tabla_absoluta.drop('Total', axis=0).drop('Total', axis=1)
        
        # Calcular porcentajes para cada grupo
        total_por_grupo = tabla_absoluta.sum(axis=1)
        
        fig = go.Figure()
        
        for fatal_type in ['Fatal', 'No Fatal']:
            if fatal_type in tabla_absoluta.columns:
                color = COLORES['fatal'] if fatal_type == 'Fatal' else COLORES['no_fatal']
                porcentajes = (tabla_absoluta[fatal_type] / total_por_grupo * 100).round(1)
                
                fig.add_trace(go.Bar(
                    name=fatal_type,
                    x=tabla_absoluta.index,
                    y=tabla_absoluta[fatal_type],
                    marker_color=color,
                    text=tabla_absoluta[fatal_type].astype(str) + '<br>(' + porcentajes.astype(str) + '%)',
                    textposition='outside',  # Cambiado a 'outside' para mejor visibilidad
                    hovertemplate=f'<b>%{{x}}</b><br>{fatal_type}: %{{y}} casos<extra></extra>'
                ))
        
        # Calcular el máximo valor para ajustar el margen superior
        max_valor = tabla_absoluta.max().max()
        
        fig.update_layout(
            title="Grupos de Edad - Condicionado por Fatalidad",
            xaxis_title="Grupo de Edad",
            yaxis_title="Número de Ataques",
            barmode='group',
            showlegend=True,
            margin=dict(t=100, b=100),
            height=500
        )
        
        # Ajustar rango del eje Y para dar espacio a las etiquetas
        fig.update_yaxes(range=[0, max_valor * 1.15])
        
    else:
        # Usar analizar_frecuencias de utils
        tabla_edad = utils.analizar_frecuencias(df, 'age_group', excluir_desconocido=True)
        
        fig = px.bar(
            tabla_edad,
            x='Categoria',
            y='Frecuencia Absoluta',
            title="Distribución de Ataques por Grupo de Edad",
            labels={'Categoria': 'Grupo de Edad', 'Frecuencia Absoluta': 'Número de Ataques'},
            color='Frecuencia Absoluta',
            color_continuous_scale=PALETA_SECUENCIAL,
            text='Frecuencia Relativa %'  # Mostrar porcentajes en barras
        )
        
        # Mejorar el formato de las etiquetas
        fig.update_traces(
            texttemplate='%{y}<br>(%{text}%)',
            textposition='outside'
        )
        
        # Ajustar márgenes y altura
        fig.update_layout(
            margin=dict(t=100, b=100),
            height=500
        )
        
        # Ajustar rango del eje Y
        max_valor = tabla_edad['Frecuencia Absoluta'].max()
        fig.update_yaxes(range=[0, max_valor * 1.15])
    
    return fig

def grafico_temporada_interactivo(condicionar_fatalidad: bool = False) -> go.Figure:
    """Gráfico de temporadas usando funciones de utils"""
    df = load_and_clean_data1()
    
    if condicionar_fatalidad:
        # Usar crear_tablas_doble_entrada de utils
        tablas = utils.crear_tablas_doble_entrada(df, 'season_clean', 'is_fatal_cat')
        
        if not tablas:
            return go.Figure()
        
        tabla_absoluta = tablas['absoluta']
        tabla_absoluta = tabla_absoluta.drop('Total', axis=0).drop('Total', axis=1)
        
        # Calcular porcentajes para cada temporada
        total_por_temporada = tabla_absoluta.sum(axis=1)
        
        fig = go.Figure()
        
        for fatal_type in ['Fatal', 'No Fatal']:
            if fatal_type in tabla_absoluta.columns:
                color = COLORES['fatal'] if fatal_type == 'Fatal' else COLORES['no_fatal']
                porcentajes = (tabla_absoluta[fatal_type] / total_por_temporada * 100).round(1)
                
                fig.add_trace(go.Bar(
                    name=fatal_type,
                    x=tabla_absoluta.index,
                    y=tabla_absoluta[fatal_type],
                    marker_color=color,
                    text=tabla_absoluta[fatal_type].astype(str) + '<br>(' + porcentajes.astype(str) + '%)',
                    textposition='outside',  # Cambiado a 'outside' para mejor visibilidad
                    hovertemplate=f'<b>%{{x}}</b><br>{fatal_type}: %{{y}} casos<extra></extra>'
                ))
        
        # Calcular el máximo valor para ajustar el margen superior
        max_valor = tabla_absoluta.max().max()
        
        fig.update_layout(
            title="Ataques por Temporada - Condicionado por Fatalidad",
            xaxis_title="Temporada",
            yaxis_title="Número de Ataques",
            barmode='group',
            showlegend=True,
            xaxis={'categoryorder': 'array', 'categoryarray': ['Primavera', 'Verano', 'Otoño', 'Invierno']},
            margin=dict(t=100, b=100),
            height=500
        )
        
        # Ajustar rango del eje Y para dar espacio a las etiquetas
        fig.update_yaxes(range=[0, max_valor * 1.15])
        
    else:
        # Usar analizar_frecuencias de utils
        tabla_temporada = utils.analizar_frecuencias(df, 'season_clean', excluir_desconocido=True)
        
        fig = px.bar(
            tabla_temporada,
            x='Categoria',
            y='Frecuencia Absoluta',
            title="Distribución de Ataques por Temporada",
            labels={'Categoria': 'Temporada', 'Frecuencia Absoluta': 'Número de Ataques'},
            color='Frecuencia Absoluta',
            color_continuous_scale=PALETA_SECUENCIAL,
            text='Frecuencia Relativa %',  # Mostrar porcentajes en barras
            category_orders={'Categoria': ['Primavera', 'Verano', 'Otoño', 'Invierno']}
        )
        
        # Mejorar el formato de las etiquetas
        fig.update_traces(
            texttemplate='%{y}<br>(%{text}%)',
            textposition='outside'
        )
        
        # Ajustar márgenes y altura
        fig.update_layout(
            margin=dict(t=100, b=100),
            height=500
        )
        
        # Ajustar rango del eje Y
        max_valor = tabla_temporada['Frecuencia Absoluta'].max()
        fig.update_yaxes(range=[0, max_valor * 1.15])
    
    return fig