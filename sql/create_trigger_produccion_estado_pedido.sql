DROP TRIGGER IF EXISTS after_update_produccion_estado_pedido$$ DELIMITER $$

-- Trigger: actualiza el estado del pedido segun el estado de sus producciones.
--
-- Bloque A: cuando una produccion pasa a 'en proceso', el pedido asociado
--           (si esta en 'Pendiente') pasa a 'En Proceso'.
--
-- Bloque B: cuando una produccion pasa a 'completado' y TODAS las producciones
--           del pedido estan completadas, el pedido pasa a 'Terminado' y se
--           registra automaticamente la Venta con su DetalleVenta.
--
-- Las producciones sin pedido asociado (standalone) son ignoradas.

CREATE TRIGGER after_update_produccion_estado_pedido
AFTER UPDATE ON produccion
FOR EACH ROW
BEGIN
    DECLARE v_pedido_id    INT          DEFAULT NULL;
    DECLARE v_total_prod   INT          DEFAULT 0;
    DECLARE v_completadas  INT          DEFAULT 0;
    DECLARE v_cliente_id   INT          DEFAULT NULL;
    DECLARE v_tipo_cliente VARCHAR(20)  DEFAULT 'retail';
    DECLARE v_venta_id     INT          DEFAULT 0;

    -- Buscar el pedido vinculado a esta produccion (puede no existir)
    SELECT id_pedido INTO v_pedido_id
    FROM pedido_produccion
    WHERE id_produccion = NEW.id_produccion
    LIMIT 1;

    -- Si no hay pedido asociado, no hay nada que hacer
    IF v_pedido_id IS NOT NULL THEN

        -- ----------------------------------------------------------------
        -- Bloque A: Pedido pasa a "En Proceso"
        -- ----------------------------------------------------------------
        IF NEW.estado = 'en proceso' AND OLD.estado <> 'en proceso' THEN
            UPDATE pedidos
            SET estado = 'En Proceso'
            WHERE id = v_pedido_id
              AND estado = 'Pendiente';
        END IF;

        -- ----------------------------------------------------------------
        -- Bloque B: Pedido pasa a "Terminado" + crear Venta
        -- ----------------------------------------------------------------
        IF NEW.estado = 'completado' AND OLD.estado <> 'completado' THEN

            -- Total de producciones vinculadas al pedido
            SELECT COUNT(*) INTO v_total_prod
            FROM pedido_produccion
            WHERE id_pedido = v_pedido_id;

            -- Producciones ya completadas del pedido
            SELECT COUNT(*) INTO v_completadas
            FROM pedido_produccion pp
            JOIN produccion p ON pp.id_produccion = p.id_produccion
            WHERE pp.id_pedido = v_pedido_id
              AND p.estado = 'completado';

            -- Si TODAS estan completadas, cerrar el pedido y registrar venta
            IF v_total_prod > 0 AND v_total_prod = v_completadas THEN

                UPDATE pedidos
                SET estado = 'Terminado'
                WHERE id = v_pedido_id;

                SELECT p.cliente_id, c.tipo
                INTO v_cliente_id, v_tipo_cliente
                FROM pedidos p
                JOIN clientes c ON c.id = p.cliente_id
                WHERE p.id = v_pedido_id;

                INSERT INTO venta (id_cliente, id_pedido, fecha, cancelada, tipo)
                VALUES (v_cliente_id, v_pedido_id, NOW(), FALSE, v_tipo_cliente);

                SET v_venta_id = LAST_INSERT_ID();

                INSERT INTO detalle_venta (id_venta, id_receta, cantidad)
                SELECT v_venta_id,
                       receta_id,
                       CAST(total_unidades AS SIGNED)
                FROM pedido_detalle
                WHERE pedido_id = v_pedido_id;

            END IF;
        END IF;

    END IF;
END$$

DELIMITER;