DROP TRIGGER IF EXISTS after_insert_produccion_movimiento_insumos$$

DELIMITER $$

CREATE TRIGGER after_insert_produccion_movimiento_insumos
AFTER INSERT ON produccion
FOR EACH ROW
BEGIN
    DECLARE v_conteo_insumos INT;
    DECLARE v_usuario_id INT;

    SELECT COUNT(*) INTO v_conteo_insumos 
    FROM receta_detalle 
    WHERE receta_id = NEW.id_receta;

    IF v_conteo_insumos = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La receta no tiene ingredientes configurados. No se puede registrar la producción.';
    END IF;

    -- No crear salida para producciones retail (pedidos),
    -- ya que los movimientos virtuales se manejan desde la aplicación
    IF NEW.es_retail = FALSE THEN
        SELECT COALESCE(MIN(id), 1) INTO v_usuario_id FROM usuario LIMIT 1;

        INSERT INTO movimientos_materia_prima (
            materia_prima_id,
            tipo,
            cantidad,
            fecha,
            motivo,
            usuario_id,
            produccion_id
        )
        SELECT 
            rd.materia_prima_id,
            'salida',
            (rd.cantidad * NEW.cantidad), 
            NOW(),
            CONCAT('Salida por inicio de Producción #', NEW.id_produccion),
            v_usuario_id,
            NEW.id_produccion
        FROM receta_detalle rd
        WHERE rd.receta_id = NEW.id_receta;
    END IF;

END$$

DELIMITER;