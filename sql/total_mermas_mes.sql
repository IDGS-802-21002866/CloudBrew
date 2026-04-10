CREATE OR REPLACE VIEW vw_mermas_por_mes AS
SELECT 
    YEAR(m.fecha_registro) AS anio,
    MONTH(m.fecha_registro) AS mes,
    SUM(m.cantidad) AS total_mermas
FROM mermas_materia_prima m
WHERE m.activo = 1
GROUP BY anio, mes
ORDER BY anio DESC, mes DESC
LIMIT 1;