-- ============================================================
-- CloudBrew — Roles y Usuarios de Base de Datos
-- Motor: MySQL 8+
-- Uso: Ejecutar una sola vez sobre la base de datos de producción
--      como usuario root o con privilegio GRANT OPTION.
--
-- Ajusta el nombre de la base de datos en @db si es necesario.
-- Las contraseñas están marcadas como CAMBIAR; reemplázalas
-- antes de ejecutar en producción.
-- ============================================================

SET @db = 'cloud_brew';
-- <- cambia si tu BD tiene otro nombre

-- ============================================================
-- 1. ELIMINAR ROLES ANTERIORES (re-runnable)
-- ============================================================
DROP ROLE IF EXISTS 'rol_admin' @'%';

DROP ROLE IF EXISTS 'rol_almacen' @'%';

DROP ROLE IF EXISTS 'rol_compras' @'%';

DROP ROLE IF EXISTS 'rol_ventas' @'%';

DROP ROLE IF EXISTS 'rol_cliente' @'%';

DROP ROLE IF EXISTS 'rol_app' @'%';

-- ============================================================
-- 2. CREAR ROLES DE BD
-- ============================================================
CREATE ROLE IF NOT EXISTS 'rol_admin' @'%';

CREATE ROLE IF NOT EXISTS 'rol_almacen' @'%';

CREATE ROLE IF NOT EXISTS 'rol_compras' @'%';

CREATE ROLE IF NOT EXISTS 'rol_ventas' @'%';

CREATE ROLE IF NOT EXISTS 'rol_cliente' @'%';

-- Rol base que hereda la aplicación Flask (conexión general)
CREATE ROLE IF NOT EXISTS 'rol_app' @'%';

-- ============================================================
-- 3. PERMISOS POR ROL
-- ============================================================

-- ── 3.1  rol_app  ────────────────────────────────────────────
-- Permisos mínimos comunes a toda conexión de la aplicación
-- (lectura de catálogos de sesión y login)
GRANT SELECT ON cloud_brew.rol TO 'rol_app' @'%';

GRANT SELECT ON cloud_brew.tipo_medida TO 'rol_app' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.`session` TO 'rol_app' @'%';

GRANT
SELECT,
INSERT
    ON cloud_brew.bitacora_login TO 'rol_app' @'%';

GRANT SELECT, UPDATE ON cloud_brew.usuario TO 'rol_app' @'%';

-- ── 3.2  rol_admin  ──────────────────────────────────────────
-- Acceso completo (SELECT, INSERT, UPDATE, DELETE) a todas las tablas.
-- Incluye todos los permisos de los demás roles.

GRANT ALL PRIVILEGES ON cloud_brew.rol TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.usuario TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.bitacora_login TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.tipo_medida TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.unidad_medida TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.materias_primas TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.presentaciones TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.proveedor TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.compra TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.detalle_compra TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.solicitud_compra TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.movimientos_materia_prima TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.mermas_materia_prima TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.recetas TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.receta_detalle TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.procesos_productivos TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.procesos_receta TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.produccion TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.produccion_proceso TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.lotes_produccion TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.movimientos_receta TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.mermas_producto_terminado TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.clientes TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.pedidos TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.pedido_detalle TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.pedido_produccion TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.venta TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.detalle_venta TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.producto_venta TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.reserva_stock TO 'rol_admin' @'%';

GRANT ALL PRIVILEGES ON cloud_brew.`session` TO 'rol_admin' @'%';
-- Vistas
GRANT SELECT ON cloud_brew.vw_mermas_por_mes TO 'rol_admin' @'%';

GRANT SELECT ON cloud_brew.vw_ventas_por_mes TO 'rol_admin' @'%';

GRANT SELECT ON cloud_brew.vw_utilidad_producto TO 'rol_admin' @'%';

GRANT
SELECT ON cloud_brew.vw_top_producto_producido TO 'rol_admin' @'%';

GRANT
SELECT ON cloud_brew.vw_top_producto_vendido TO 'rol_admin' @'%';

-- ── 3.3  rol_almacen  ────────────────────────────────────────
-- Módulos: Materias Primas, Unidades, Presentaciones, Recetas,
--          Compras (lectura), Inventario MP, Mermas MP,
--          Inventario PT (lectura), Mermas PT,
--          Proc. Productivos, Producción, Lotes.

-- Catálogos propios (CRUD)
GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.tipo_medida TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.unidad_medida TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.materias_primas TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.presentaciones TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.recetas TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.receta_detalle TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.procesos_productivos TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.procesos_receta TO 'rol_almacen' @'%';

-- Inventario de materia prima (completo)
GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.movimientos_materia_prima TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.mermas_materia_prima TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
    ON cloud_brew.solicitud_compra TO 'rol_almacen' @'%';

-- Producción y lotes
GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.produccion TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.produccion_proceso TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
    ON cloud_brew.lotes_produccion TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
    ON cloud_brew.movimientos_receta TO 'rol_almacen' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.mermas_producto_terminado TO 'rol_almacen' @'%';

-- Lectura de compras (ver órdenes que impactan inventario)
GRANT SELECT ON cloud_brew.compra TO 'rol_almacen' @'%';

GRANT SELECT ON cloud_brew.detalle_compra TO 'rol_almacen' @'%';

GRANT SELECT ON cloud_brew.proveedor TO 'rol_almacen' @'%';

-- Lectura de inventario PT y pedidos (para saber qué producir)
GRANT SELECT ON cloud_brew.pedidos TO 'rol_almacen' @'%';

GRANT SELECT ON cloud_brew.pedido_detalle TO 'rol_almacen' @'%';

GRANT SELECT ON cloud_brew.pedido_produccion TO 'rol_almacen' @'%';

GRANT SELECT ON cloud_brew.producto_venta TO 'rol_almacen' @'%';

-- Vistas relevantes
GRANT SELECT ON cloud_brew.vw_mermas_por_mes TO 'rol_almacen' @'%';

GRANT
SELECT ON cloud_brew.vw_top_producto_producido TO 'rol_almacen' @'%';

-- ── 3.4  rol_compras  ────────────────────────────────────────
-- Módulos: Proveedores, Materias Primas (lectura+solicitud),
--          Presentaciones (lectura), Compras (CRUD), Inventario MP (lectura).

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.proveedor TO 'rol_compras' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.compra TO 'rol_compras' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.detalle_compra TO 'rol_compras' @'%';

GRANT
SELECT,
UPDATE ON cloud_brew.solicitud_compra TO 'rol_compras' @'%';

-- Lectura de catálogos necesarios para generar órdenes de compra
GRANT SELECT ON cloud_brew.materias_primas TO 'rol_compras' @'%';

GRANT SELECT ON cloud_brew.presentaciones TO 'rol_compras' @'%';

GRANT SELECT ON cloud_brew.tipo_medida TO 'rol_compras' @'%';

GRANT SELECT ON cloud_brew.unidad_medida TO 'rol_compras' @'%';

GRANT
SELECT ON cloud_brew.movimientos_materia_prima TO 'rol_compras' @'%';

-- ── 3.5  rol_ventas  ─────────────────────────────────────────
-- Módulos: Clientes, Pedidos, Ventas, Costos,
--          Productos de Venta, Inventario PT (lectura).

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.clientes TO 'rol_ventas' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.pedidos TO 'rol_ventas' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.pedido_detalle TO 'rol_ventas' @'%';

GRANT SELECT, UPDATE ON cloud_brew.venta TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.detalle_venta TO 'rol_ventas' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.producto_venta TO 'rol_ventas' @'%';

GRANT
SELECT,
INSERT
,
UPDATE ON cloud_brew.reserva_stock TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.pedido_produccion TO 'rol_ventas' @'%';

-- Lectura de inventario PT para verificar disponibilidad
GRANT SELECT ON cloud_brew.lotes_produccion TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.movimientos_receta TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.recetas TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.presentaciones TO 'rol_ventas' @'%';

-- Vistas de costos y utilidad
GRANT SELECT ON cloud_brew.vw_ventas_por_mes TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.vw_utilidad_producto TO 'rol_ventas' @'%';

GRANT
SELECT ON cloud_brew.vw_top_producto_vendido TO 'rol_ventas' @'%';

GRANT SELECT ON cloud_brew.vw_mermas_por_mes TO 'rol_ventas' @'%';

-- ── 3.6  rol_cliente  ────────────────────────────────────────
-- Acceso exclusivo al portal de tienda.
-- Solo puede ver catálogo, gestionar su carrito y ver sus pedidos/ventas.

GRANT SELECT ON cloud_brew.producto_venta TO 'rol_cliente' @'%';

GRANT SELECT ON cloud_brew.recetas TO 'rol_cliente' @'%';

GRANT SELECT ON cloud_brew.presentaciones TO 'rol_cliente' @'%';

-- Carrito de compras
GRANT
SELECT,
INSERT
,
UPDATE,
DELETE ON cloud_brew.reserva_stock TO 'rol_cliente' @'%';

-- Sus propios pedidos y ventas (filtrado por app, no por BD)
GRANT SELECT, INSERT ON cloud_brew.pedidos TO 'rol_cliente' @'%';

GRANT
SELECT,
INSERT
    ON cloud_brew.pedido_detalle TO 'rol_cliente' @'%';

GRANT SELECT ON cloud_brew.venta TO 'rol_cliente' @'%';

GRANT SELECT ON cloud_brew.detalle_venta TO 'rol_cliente' @'%';

-- Su propio perfil de usuario
GRANT SELECT, UPDATE ON cloud_brew.usuario TO 'rol_cliente' @'%';

GRANT SELECT, UPDATE ON cloud_brew.clientes TO 'rol_cliente' @'%';

-- ============================================================
-- 4. USUARIOS DE BD Y ASIGNACIÓN DE ROLES
-- ============================================================
-- IMPORTANTE: cambia las contraseñas antes de ejecutar en producción.

-- Usuario de la aplicación Flask (usa rol_app como base)
DROP USER IF EXISTS 'usr_app' @'%';

CREATE USER 'usr_app' @'%' IDENTIFIED BY '23D759q29IiZ';

GRANT 'rol_app' @'%' TO 'usr_app' @'%';
-- Activa el rol por defecto al conectar (MySQL 8+)
ALTER USER 'usr_app' @'%' DEFAULT ROLE 'rol_app' @'%';

-- Usuario administrador del ERP
DROP USER IF EXISTS 'usr_admin' @'%';

CREATE USER 'usr_admin' @'%' IDENTIFIED BY 'CAMBIAR_contrasena_admin';

GRANT 'rol_app' @'%', 'rol_admin' @'%' TO 'usr_admin' @'%';

ALTER USER 'usr_admin' @'%' DEFAULT ROLE ALL;

-- Usuario de almacén
DROP USER IF EXISTS 'usr_almacen' @'%';

CREATE USER 'usr_almacen' @'%' IDENTIFIED BY 'CAMBIAR_contrasena_almacen';

GRANT 'rol_app' @'%', 'rol_almacen' @'%' TO 'usr_almacen' @'%';

ALTER USER 'usr_almacen' @'%' DEFAULT ROLE ALL;

-- Usuario de compras
DROP USER IF EXISTS 'usr_compras' @'%';

CREATE USER 'usr_compras' @'%' IDENTIFIED BY 'CAMBIAR_contrasena_compras';

GRANT 'rol_app' @'%', 'rol_compras' @'%' TO 'usr_compras' @'%';

ALTER USER 'usr_compras' @'%' DEFAULT ROLE ALL;

-- Usuario de ventas
DROP USER IF EXISTS 'usr_ventas' @'%';

CREATE USER 'usr_ventas' @'%' IDENTIFIED BY 'CAMBIAR_contrasena_ventas';

GRANT 'rol_app' @'%', 'rol_ventas' @'%' TO 'usr_ventas' @'%';

ALTER USER 'usr_ventas' @'%' DEFAULT ROLE ALL;

-- Usuario del portal de tienda (clientes)
DROP USER IF EXISTS 'usr_tienda' @'%';

CREATE USER 'usr_tienda' @'%' IDENTIFIED BY 'CAMBIAR_contrasena_tienda';

GRANT 'rol_app' @'%', 'rol_cliente' @'%' TO 'usr_tienda' @'%';

ALTER USER 'usr_tienda' @'%' DEFAULT ROLE ALL;

-- ============================================================
-- 5. TRIGGER: after_insert_cliente -> crear usuario BD con rol cliente
-- ============================================================
-- Al insertar un registro en `clientes` (p.ej. desde la tienda),
-- se crea automáticamente un usuario en la tabla `usuario` de la
-- aplicación con rol=cliente y contraseña bloqueada.
-- El cliente debe usar "Recuperar contraseña" en la tienda para activarse.

DROP TRIGGER IF EXISTS after_insert_cliente;

DELIMITER $$

CREATE TRIGGER after_insert_cliente
AFTER INSERT ON clientes
FOR EACH ROW
BEGIN
    DECLARE v_rol_id INT;

    -- Evitar recursión si el INSERT viene desde el trigger inverso
    IF @creating_from_usuario_trigger IS NULL OR @creating_from_usuario_trigger != 1 THEN

        IF NOT EXISTS (SELECT 1 FROM usuario WHERE email = NEW.email) THEN

            SELECT id INTO v_rol_id FROM rol WHERE name = 'cliente' LIMIT 1;

            IF v_rol_id IS NOT NULL THEN
                SET @creating_from_cliente_trigger = 1;

                INSERT INTO usuario (
                    nombre,
                    email,
                    password,
                    activo,
                    rol_id,
                    fs_uniquifier
                )
                VALUES (
                    CONCAT(NEW.nombres, ' ', NEW.apellidos),
                    NEW.email,
                    'LOCKED',
                    1,
                    v_rol_id,
                    UUID()
                );

                SET @creating_from_cliente_trigger = 0;
            END IF;
        END IF;

    END IF;
END$$

DELIMITER;

-- ============================================================
-- 6. APLICAR CAMBIOS
-- ============================================================
FLUSH PRIVILEGES;

-- ============================================================
-- RESUMEN DE ACCESOS POR ROL
-- ============================================================
--
--  ROL           | TABLAS CON ESCRITURA (INSERT/UPDATE/DELETE)
-- ───────────────┼──────────────────────────────────────────────────────────
--  rol_admin     | Todas las tablas
--  rol_almacen   | tipo_medida, unidad_medida, materias_primas,
--                | presentaciones, recetas, receta_detalle,
--                | procesos_productivos, procesos_receta,
--                | movimientos_materia_prima, mermas_materia_prima,
--                | solicitud_compra (solo INSERT), produccion,
--                | produccion_proceso, lotes_produccion,
--                | movimientos_receta, mermas_producto_terminado
--  rol_compras   | proveedor, compra, detalle_compra, solicitud_compra
--  rol_ventas    | clientes, pedidos, pedido_detalle, venta (update),
--                | producto_venta, reserva_stock
--  rol_cliente   | reserva_stock, pedidos, pedido_detalle,
--                | usuario (solo UPDATE de su perfil), clientes (UPDATE)
--
-- ============================================================