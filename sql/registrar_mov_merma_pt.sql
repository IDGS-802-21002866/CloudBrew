DELIMITER //

DROP TRIGGER IF EXISTS after_merma_insert //

CREATE TRIGGER after_merma_insert
AFTER INSERT ON mermas_producto_terminado
FOR EACH ROW
BEGIN
    -- Insertar automáticamente el movimiento de salida
    INSERT INTO movimientos_receta (
        receta_id, 
        lote_id, 
        cantidad, 
        tipo, 
        motivo, 
        usuario_id
    )
    VALUES (
        NEW.receta_id, 
        NEW.lote_id, 
        NEW.cantidad, 
        'salida', 
        CONCAT('MERMA: ', NEW.motivo), 
        NEW.usuario_id
    ); -- <--- Aquí quité la coma que sobraba
END //

DELIMITER ;