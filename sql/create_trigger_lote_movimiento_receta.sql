DROP TRIGGER IF EXISTS after_insert_lote_movimiento_receta$$

DELIMITER $$

CREATE TRIGGER after_insert_lote_movimiento_receta
AFTER INSERT ON lotes_produccion
FOR EACH ROW
BEGIN
    DECLARE v_receta_id INT;
    DECLARE v_usuario_id INT;
    DECLARE v_tiene_pedido INT;

    -- Verificar si la produccion esta asociada a un pedido
    SELECT COUNT(*) INTO v_tiene_pedido
    FROM pedido_produccion pp
    WHERE pp.id_produccion = NEW.id_produccion;

    -- Solo registrar entrada si NO tiene pedido asociado
    IF v_tiene_pedido = 0 THEN

        SELECT p.id_receta INTO v_receta_id
        FROM produccion p
        WHERE p.id_produccion = NEW.id_produccion;

        -- Usuario del sistema (1) o NULL si no existe
        SELECT id INTO v_usuario_id
        FROM usuario
        LIMIT 1;

        IF v_usuario_id IS NULL THEN
            SET v_usuario_id = 1;
        END IF;

        INSERT INTO movimientos_receta (
            receta_id,
            tipo,
            cantidad,
            fecha,
            motivo,
            usuario_id
        )
        VALUES (
            v_receta_id,
            'entrada',
            NEW.cantidad_generada,
            NOW(),
            CONCAT('Entrada por completación de Producción #', NEW.id_produccion, ' - Lote ', NEW.codigo_lote),
            v_usuario_id
        );

    END IF;

END$$

DELIMITER;