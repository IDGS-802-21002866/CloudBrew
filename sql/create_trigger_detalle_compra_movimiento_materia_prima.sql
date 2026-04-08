DROP TRIGGER IF EXISTS after_update_detalle_compra_movimiento_materia_prima$$ DELIMITER $$

CREATE TRIGGER after_update_detalle_compra_movimiento_materia_prima
AFTER UPDATE ON detalle_compra
FOR EACH ROW
BEGIN
    DECLARE v_fecha_compra DATETIME;
    DECLARE v_usuario_id INT;
    DECLARE v_cancelada BOOLEAN DEFAULT FALSE;
    DECLARE v_cantidad_equivalente DECIMAL(18, 6);
    DECLARE v_tipo_presentacion_id INT;
    DECLARE v_tipo_materia_prima_id INT;

    IF NEW.precio_unitario < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El precio no puede ser negativo';
    END IF;

    SELECT c.fecha_compra, c.usuario_id, c.cancelada
      INTO v_fecha_compra, v_usuario_id, v_cancelada
      FROM compra c
     WHERE c.id = NEW.compra_id;

        SELECT p.cantidad_equivalente, p.tipo_medida_id
            INTO v_cantidad_equivalente, v_tipo_presentacion_id
            FROM presentaciones p
         WHERE p.id = NEW.presentacion_id;

        SELECT mp.tipo_medida_id
            INTO v_tipo_materia_prima_id
            FROM materias_primas mp
         WHERE mp.id = NEW.materia_prima_id;

        IF v_cantidad_equivalente IS NULL OR v_cantidad_equivalente <= 0 THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'La presentacion no tiene un factor de conversion valido';
        END IF;

        IF v_tipo_presentacion_id <> v_tipo_materia_prima_id THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'La presentacion no coincide con el tipo de medida de la materia prima';
        END IF;

    IF v_fecha_compra IS NOT NULL
       AND v_cancelada = FALSE
       AND NEW.precio_unitario > 0
       AND (OLD.precio_unitario IS NULL OR OLD.precio_unitario <= 0)
       AND NOT EXISTS (
           SELECT 1
             FROM movimientos_materia_prima m
            WHERE m.tipo = 'entrada'
              AND m.motivo = CONCAT('Compra #', NEW.compra_id, ' - Detalle #', NEW.id)
       )
    THEN
        INSERT INTO movimientos_materia_prima (
            materia_prima_id,
            tipo,
            cantidad,
            fecha,
            motivo,
            usuario_id,
            detalle_compra_id
        )
        VALUES (
            NEW.materia_prima_id,
            'entrada',
            NEW.cantidad * v_cantidad_equivalente,
            v_fecha_compra,
            CONCAT('Compra #', NEW.compra_id, ' - Detalle #', NEW.id),
            v_usuario_id,
            NEW.id
        );
    END IF;
END$$

DELIMITER;

DELIMITER $$

CREATE TRIGGER after_insert_merma_materia_prima
AFTER INSERT ON mermas_materia_prima
FOR EACH ROW
BEGIN
    INSERT INTO movimientos_materia_prima (
        materia_prima_id, tipo, cantidad, fecha, motivo, usuario_id
    ) VALUES (
        NEW.materia_prima_id, 'salida', NEW.cantidad, NOW(), 
        CONCAT('Merma #', NEW.id, ': ', NEW.motivo), NEW.usuario_id
    );
END$$

CREATE TRIGGER after_update_merma_materia_prima
AFTER UPDATE ON mermas_materia_prima
FOR EACH ROW
BEGIN
    IF OLD.activo = 1 AND NEW.activo = 0 THEN
        DELETE FROM movimientos_materia_prima 
        WHERE motivo LIKE CONCAT('Merma #', OLD.id, '%');
    END IF;
END$$

DELIMITER ;