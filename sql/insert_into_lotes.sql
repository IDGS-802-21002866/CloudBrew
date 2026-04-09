DROP TRIGGER IF EXISTS after_update_proceso_completar_produccion$$

DELIMITER $$

CREATE TRIGGER after_update_proceso_completar_produccion
AFTER UPDATE ON produccion_proceso
FOR EACH ROW
BEGIN
    DECLARE v_pendientes INT;
    DECLARE v_cantidad_receta FLOAT;
    DECLARE v_codigo_lote VARCHAR(100);

    IF NEW.estado = 'completado' AND OLD.estado <> 'completado' THEN
        
        SELECT COUNT(*) INTO v_pendientes
        FROM produccion_proceso
        WHERE id_produccion = NEW.id_produccion
          AND estado <> 'completado';

        IF v_pendientes = 0 THEN
            
            SELECT r.cantidad_producida INTO v_cantidad_receta
            FROM produccion p
            JOIN recetas r ON p.id_receta = r.id
            WHERE p.id_produccion = NEW.id_produccion;

            SET v_codigo_lote = DATE_FORMAT(NOW(), '%d.%m.%Y.%H.%M');

            INSERT INTO lotes_produccion (
                id_produccion,
                codigo_lote,
                fecha_produccion,
                cantidad_generada
            )
            SELECT 
                NEW.id_produccion,
                v_codigo_lote,
                CURDATE(),
                v_cantidad_receta * p.cantidad
            FROM produccion p
            WHERE p.id_produccion = NEW.id_produccion;
            
            UPDATE produccion 
            SET estado = 'completado', fecha_fin = CURDATE() 
            WHERE id_produccion = NEW.id_produccion;

        END IF;
    END IF;
END$$

DELIMITER;