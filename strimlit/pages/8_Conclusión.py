import streamlit as st
import stilez 

st.set_page_config(
    page_title="Conclusión - Ataques de Tiburón",
    page_icon="🦈",
    layout="wide"
)

stilez.aplicar_estilos_globales()

# titulo principal
st.title("Conclusiones y Recomendaciones")
st.markdown("---")


# contenido principal
st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
En el presente capitulo se pretende exponer las conclusiones obtenidas en la investigación las cuales se desglosarán según los objetivos señalados al inicio del estudio, así como las recomendaciones para mitigar los problemas planteados.

</div>
""", unsafe_allow_html=True)

st.markdown("#### Investigar la tasa global de fatalidad para establecer la proporción de ataques mortales.")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: De un total de 5001 incidentes aproximadamente 1 de cada 5 ataques fueron fatales si bien existen altas probabilidades de supervivencia, la tasa de fatalidad sigue siendo considerable.
            
•	Recomendación: Fomentar la necesidad de seguir protocolos de seguridad en el mar al público, así como campañas de capacitación para socorristas.

</div>
""", unsafe_allow_html=True)

st.markdown("#### Evaluar el riesgo por actividad para identificar, mediante la frecuencia absoluta y relativa, la actividad humana (activity) que concentra el mayor número de ataques.")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: Podemos observar una distribución de riesgo principalmente concentrada en 4 actividades surfear, bodyboarding, pesca y nadar. Por el otro lado actividades como flotar, remar y caer por la borda de una embarcación, presentan una frecuencia de ataques casi insignificante. Lo que nos muestra que el riesgo de sufrir un ataque está directamente relacionado con la actividad realizada.
            
•	Recomendación: Promover la concientización y campañas de seguridad principalmente en las comunidades surfista, bodyboarders y pescadores.


</div>
""", unsafe_allow_html=True)

st.markdown("#### Examinar los países para ubicar los de mayor incidencia y su distribución de casos fatales.")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: Los incidentes se encuentran concentrados predominantemente en tres países, Estados Unidos registrando, Australia y Sudáfrica representando en total casi el 70% de ataques a nivel mundial.

•	Recomendación: Priorizar los recursos, estrategias de mitigación y seguridad en estos tres países principales, sin descuidar la vigilancia en las demás naciones.



</div>
""", unsafe_allow_html=True)

st.markdown("#### Examinar la distribución por grupos de edad para identificar patrones de vulnerabilidad según la fatalidad.")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: El perfil de las victimas tiende a ser joven, un 77,99% se encuentra entre las edades de 0 a 30 años y podemos observar una disminución de riesgo conforme aumenta la edad con tan solo un 8,22% de las victimas superando los 46 años.

•	Recomendación: Intervenciones focalizadas en la población joven (0 a 30 años) además de educación preventiva en centros educativos costeros.




</div>
""", unsafe_allow_html=True)

st.markdown("####     Evaluar las estaciones del año para determinar las más peligrosas y su asociación con la fatalidad.")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: La estación del año con mayor cantidad de ataques de tiburón fue invierno con un 29,31% mientras que las demás estaciones del año se encuentran relativamente equilibradas.

•	Recomendación: Reforzar medidas preventivas durante invierno en regiones de alto riesgo además de coordinar con autoridades turísticas para educación en periodos críticos.




</div>
""", unsafe_allow_html=True)

st.markdown("####     Examinar el riesgo cruzado para discriminar si existe una mayor proporción de fatalidad al cruzar los datos de la actividad (activity) con la gravedad del incidente (is_fatal).")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: Existe una gran disparidad de proporción de fatalidad entre las actividades, por ejemplo, actividades percibidas generalmente como menos riesgosas como bañarse o nadar presentan una alta tasa de fatalidad con 42,4% y 37,5% respectivamente. Sin embargo, actividades como surfear la actividad con más incidentes reportados presenta una tasa de fatalidad de las más bajas con 6,55% lo que descarta una correlación entre la frecuencia de un incidente y su letalidad.

•	Recomendación: Enfocar la prevención en las actividades con mayor riesgo como bañarse y nadar, ya que son actividades comunes con alta fatalidad.




</div>
""", unsafe_allow_html=True)

st.markdown("####     Examinar la relación entre variables y fatalidad para analizar cómo la actividad, país, edad y estación se asocian con la letalidad de los incidentes mediante tablas de contingencia.")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
•	Conclusión: Confirmamos que la actividad más mortal fue nadar, el país más afectado fue Australia, el grupo de edad más vulnerable fueron los jóvenes de 19 a 30 años y la estación más crítica fue el verano

•	Recomendación: Focalizar prevención en nadadores, reforzar las medidas de seguridad de Australia y realizar campañas dirigidas a jóvenes adultos (19-30 años) en épocas criticas como el verano.





</div>
""", unsafe_allow_html=True)

st.markdown("#### Conclusión general")

st.markdown("""
<div style='text-align: justify; line-height: 1.6; font-size: 16px;'>
    
La mayoría de los ataques de tiburones no son fatales, lo que ofrece una perspectiva más tranquilizadora, sin embargo, ciertas actividades y grupos poblacionales presentan un riesgo elevado y requieren atención prioritaria. Es necesario aumentar los protocolos de seguridad y fortalecer la educación en comunidades costeras.



</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Análisis Descriptivo de Ataques de Tiburón | Conclusión")
