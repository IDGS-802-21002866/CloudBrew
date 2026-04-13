CREATE OR REPLACE VIEW vw_ventas_por_mes AS
SELECT 
    YEAR(p.fecha_registro) AS anio,
    MONTH(p.fecha_registro) AS mes,
    SUM(pd.total_unidades) AS total_unidades_vendidas,
    COUNT(DISTINCT p.id) AS total_pedidos
FROM pedidos p
JOIN pedido_detalle pd ON pd.pedido_id = p.id
WHERE p.activo = 1
GROUP BY anio, mes
ORDER BY anio DESC, mes DESC
LIMIT 1;