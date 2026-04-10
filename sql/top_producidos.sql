CREATE OR REPLACE VIEW vw_top_producto_producido AS
SELECT 
    r.id,
    r.nombre,
    SUM(p.cantidad) AS total_producido
FROM produccion p
JOIN recetas r ON r.id = p.id_receta
GROUP BY r.id, r.nombre
ORDER BY total_producido DESC;