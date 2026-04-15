CREATE OR REPLACE VIEW vw_top_producto_vendido AS
SELECT r.id, r.nombre, SUM(pd.total_unidades) AS total_vendido
FROM
    pedido_detalle pd
    JOIN producto_venta pv ON pv.id = pd.producto_venta_id
    JOIN recetas r ON r.id = pv.receta_id
GROUP BY
    r.id,
    r.nombre
ORDER BY total_vendido DESC
LIMIT 1;