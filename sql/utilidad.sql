CREATE OR REPLACE VIEW vw_costo_promedio_mp AS
SELECT dc.materia_prima_id, AVG(dc.precio_unitario) AS costo_promedio
FROM detalle_compra dc
    JOIN compra c ON dc.compra_id = c.id
WHERE
    c.cancelada = 0S
    AND c.fecha_compra >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY
    dc.materia_prima_id;

CREATE OR REPLACE VIEW vw_costo_receta AS
SELECT r.id AS receta_id, r.nombre, SUM(
        rd.cantidad * IFNULL(v.costo_promedio, 0)
    ) AS costo_total
FROM
    recetas r
    JOIN receta_detalle rd ON r.id = rd.receta_id
    LEFT JOIN vw_costo_promedio_mp v ON rd.materia_prima_id = v.materia_prima_id
GROUP BY
    r.id,
    r.nombre;

CREATE OR REPLACE VIEW vw_ventas_receta AS
SELECT
    pv.receta_id,
    SUM(pd.total_unidades) AS unidades_vendidas,
    AVG(pv.precio_venta) AS precio_venta_promedio
FROM
    pedido_detalle pd
    JOIN producto_venta pv ON pv.id = pd.producto_venta_id
    JOIN pedidos p ON pd.pedido_id = p.id
WHERE
    p.activo = 1
GROUP BY
    pv.receta_id;

CREATE OR REPLACE VIEW vw_utilidad_producto AS
SELECT
    r.receta_id,
    r.nombre,
    r.costo_total,
    IFNULL(v.precio_venta_promedio, 0) AS precio_venta,
    v.unidades_vendidas,
    (
        v.unidades_vendidas * IFNULL(v.precio_venta_promedio, 0)
    ) AS ingresos,
    (
        v.unidades_vendidas * r.costo_total
    ) AS costo_total_vendido,
    (
        (
            v.unidades_vendidas * IFNULL(v.precio_venta_promedio, 0)
        ) - (
            v.unidades_vendidas * r.costo_total
        )
    ) AS utilidad
FROM
    vw_costo_receta r
    LEFT JOIN vw_ventas_receta v ON r.receta_id = v.receta_id;