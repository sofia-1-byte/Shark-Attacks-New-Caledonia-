-- Ataques de tiburón por estación del año

CREATE VIEW vista_ataques_por_estacion AS
SELECT 
    season as estacion,
    COUNT(*) as cantidad_ataques,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shark_attackdatos 
    WHERE season IS NOT NULL AND season != 'Desconocido')), 2) as porcentaje
FROM shark_attackdatos 
WHERE season IS NOT NULL AND season != 'Desconocido'
GROUP BY season
ORDER BY cantidad_ataques DESC;

-- Top 5 actividades con más ataques fatales

CREATE VIEW vista_top5_actividades_fatales AS
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

-- Ataques por fase lunar

CREATE VIEW vista_ataques_por_fase_lunar AS
SELECT 
    moon_phase as fase_lunar,
    COUNT(*) as cantidad_ataques,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shark_attackdatos 
    WHERE moon_phase IS NOT NULL AND moon_phase != 'Desconocido')), 2) as porcentaje
FROM shark_attackdatos 
WHERE moon_phase IS NOT NULL AND moon_phase != 'Desconocido'
GROUP BY moon_phase
ORDER BY cantidad_ataques DESC;

-- Especies implicadas con categoria de conservacion

CREATE VIEW vista_especies_conservacion AS
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
	
-- Ataques fatales por decada

CREATE VIEW vista_ataques_fatales_por_decada AS
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