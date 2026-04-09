DROP TRIGGER IF EXISTS after_insert_produccion_movimiento_insumos$$

DELIMITER $$

CREATE TRIGGER after_insert_produccion_movimiento_insumos
AFTER INSERT ON produccion
FOR EACH ROW
BEGIN
    DECLARE v_conteo_insumos INT;

    SELECT COUNT(*) INTO v_conteo_insumos 
    FROM detalle_receta 
    WHERE receta_id = NEW.id_receta;

    IF v_conteo_insumos = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La receta no tiene ingredientes configurados. No se puede registrar la producción.';
    END IF;

    INSERT INTO movimientos_materia_prima (
        materia_prima_id,
        tipo,
        cantidad,
        fecha,
        motivo,
        lote_produccion_id
    )
    SELECT 
        dr.materia_prima_id,
        'salida',
        (dr.cantidad * NEW.cantidad), 
        NOW(),
        CONCAT('Salida por inicio de Producción #', NEW.id_produccion),
        NEW.id_produccion
    FROM detalle_receta dr
    WHERE dr.receta_id = NEW.id_receta;

END$$

DELIMITER ;