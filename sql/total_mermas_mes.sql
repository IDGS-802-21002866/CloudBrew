CREATE OR REPLACE VIEW vw_mermas_por_mes AS
SELECT 
    YEAR(m.fecha_registro) AS anio,
    MONTH(m.fecha_registro) AS mes,
    SUM(m.cantidad) AS total_mermas_unidades,
    -- Calculamos el costo multiplicando la cantidad de merma por el precio unitario
    -- Usamos COALESCE para que si no hay precio registrado, el valor sea 0
    ROUND(SUM(m.cantidad * COALESCE(
        (SELECT dc.precio_unitario 
         FROM detalle_compra dc 
         WHERE dc.materia_prima_id = m.materia_prima_id 
         ORDER BY dc.id DESC LIMIT 1), 0)
    ), 2) AS costo_total_mermas
FROM mermas_materia_prima m
WHERE m.activo = 1
GROUP BY anio, mes
ORDER BY anio DESC, mes DESC;