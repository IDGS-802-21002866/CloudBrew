CREATE DATABASE  IF NOT EXISTS `cloud_brew` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cloud_brew`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: cloud_brew
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bitacora_login`
--

DROP TABLE IF EXISTS `bitacora_login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bitacora_login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `hora` datetime NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `auth` tinyint(1) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `calle_numero` varchar(150) NOT NULL,
  `colonia` varchar(100) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `estado` varchar(100) NOT NULL,
  `codigo_postal` varchar(10) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `compra`
--

DROP TABLE IF EXISTS `compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_registro` datetime NOT NULL,
  `fecha_compra` datetime DEFAULT NULL,
  `cancelada` tinyint(1) NOT NULL,
  `proveedor_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `actualizado_por` varchar(100) DEFAULT NULL,
  `solicitud_compra_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `solicitud_compra_id` (`solicitud_compra_id`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `compra_ibfk_3` FOREIGN KEY (`solicitud_compra_id`) REFERENCES `solicitud_compra` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detalle_compra`
--

DROP TABLE IF EXISTS `detalle_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compra_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `presentacion_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compra_id` (`compra_id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `presentacion_id` (`presentacion_id`),
  CONSTRAINT `detalle_compra_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compra` (`id`),
  CONSTRAINT `detalle_compra_ibfk_2` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `detalle_compra_ibfk_3` FOREIGN KEY (`presentacion_id`) REFERENCES `presentaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_update_detalle_compra_movimiento_materia_prima` AFTER UPDATE ON `detalle_compra` FOR EACH ROW BEGIN
    DECLARE v_fecha_compra DATETIME;
    DECLARE v_usuario_id INT;
    DECLARE v_cancelada BOOLEAN DEFAULT FALSE;
    DECLARE v_cantidad_equivalente DECIMAL(18, 6);
    DECLARE v_tipo_presentacion_id INT;
    DECLARE v_tipo_materia_prima_id INT;
    DECLARE v_solicitud_compra_id INT DEFAULT NULL;
    DECLARE v_solicitud_origen VARCHAR(20) DEFAULT NULL;
    DECLARE v_solicitud_cantidad DECIMAL(18, 6) DEFAULT 0;
    DECLARE v_cantidad_base DECIMAL(18, 6);
    DECLARE v_cantidad_entrada DECIMAL(18, 6);

    IF NEW.precio_unitario < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El precio no puede ser negativo';
    END IF;

    SELECT c.fecha_compra, c.usuario_id, c.cancelada, c.solicitud_compra_id
      INTO v_fecha_compra, v_usuario_id, v_cancelada, v_solicitud_compra_id
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
        SET v_cantidad_base = NEW.cantidad * v_cantidad_equivalente;
        SET v_cantidad_entrada = v_cantidad_base;

        -- Si la compra esta vinculada a una solicitud retail (pedido),
        -- solo agregar el excedente al inventario
        IF v_solicitud_compra_id IS NOT NULL THEN
            SELECT sc.origen, sc.cantidad
              INTO v_solicitud_origen, v_solicitud_cantidad
              FROM solicitud_compra sc
             WHERE sc.id = v_solicitud_compra_id
               AND sc.materia_prima_id = NEW.materia_prima_id;

            IF v_solicitud_origen = 'retail' THEN
                IF v_cantidad_base > v_solicitud_cantidad THEN
                    SET v_cantidad_entrada = v_cantidad_base - v_solicitud_cantidad;
                ELSE
                    SET v_cantidad_entrada = 0;
                END IF;
            END IF;
        END IF;

        IF v_cantidad_entrada > 0 THEN
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
                v_cantidad_entrada,
                v_fecha_compra,
                CONCAT('Compra #', NEW.compra_id, ' - Detalle #', NEW.id),
                v_usuario_id,
                NEW.id
            );
        END IF;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `detalle_venta`
--

DROP TABLE IF EXISTS `detalle_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `id_producto_venta` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_producto_venta` (`id_producto_venta`),
  KEY `id_venta` (`id_venta`),
  CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_producto_venta`) REFERENCES `producto_venta` (`id`),
  CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lotes_produccion`
--

DROP TABLE IF EXISTS `lotes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lotes_produccion` (
  `id_lote` int NOT NULL AUTO_INCREMENT,
  `id_produccion` int NOT NULL,
  `codigo_lote` varchar(100) NOT NULL,
  `fecha_produccion` date DEFAULT NULL,
  `cantidad_generada` float DEFAULT NULL,
  PRIMARY KEY (`id_lote`),
  KEY `id_produccion` (`id_produccion`),
  CONSTRAINT `lotes_produccion_ibfk_1` FOREIGN KEY (`id_produccion`) REFERENCES `produccion` (`id_produccion`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_lote_movimiento_receta` AFTER INSERT ON `lotes_produccion` FOR EACH ROW BEGIN

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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `materias_primas`
--

DROP TABLE IF EXISTS `materias_primas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias_primas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `tipo_medida_id` int NOT NULL,
  `stock_minimo` float NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `tipo_medida_id` (`tipo_medida_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `materias_primas_ibfk_1` FOREIGN KEY (`tipo_medida_id`) REFERENCES `tipo_medida` (`id`),
  CONSTRAINT `materias_primas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mermas_materia_prima`
--

DROP TABLE IF EXISTS `mermas_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mermas_materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia_prima_id` int NOT NULL,
  `cantidad` float NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `usuario_id` int NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `mermas_materia_prima_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `mermas_materia_prima_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_merma_materia_prima` AFTER INSERT ON `mermas_materia_prima` FOR EACH ROW BEGIN

    INSERT INTO movimientos_materia_prima (

        materia_prima_id, tipo, cantidad, fecha, motivo, merma_materia_prima_id, usuario_id

    ) VALUES (

        NEW.materia_prima_id, 'salida', NEW.cantidad, NOW(), 

        CONCAT('Merma #', NEW.id, ': ', NEW.motivo), NEW.id, NEW.usuario_id

    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_update_merma_materia_prima` AFTER UPDATE ON `mermas_materia_prima` FOR EACH ROW BEGIN

    IF OLD.activo = 1 AND NEW.activo = 0 THEN

        DELETE FROM movimientos_materia_prima 

        WHERE merma_materia_prima_id = OLD.id;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `mermas_producto_terminado`
--

DROP TABLE IF EXISTS `mermas_producto_terminado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mermas_producto_terminado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int NOT NULL,
  `lote_id` int DEFAULT NULL,
  `cantidad` float NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `usuario_id` int NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_id` (`lote_id`),
  KEY `receta_id` (`receta_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `mermas_producto_terminado_ibfk_1` FOREIGN KEY (`lote_id`) REFERENCES `lotes_produccion` (`id_lote`),
  CONSTRAINT `mermas_producto_terminado_ibfk_2` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `mermas_producto_terminado_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `movimientos_materia_prima`
--

DROP TABLE IF EXISTS `movimientos_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia_prima_id` int NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `cantidad` float NOT NULL,
  `fecha` datetime NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  `detalle_compra_id` int DEFAULT NULL,
  `lote_produccion_id` int DEFAULT NULL,
  `merma_materia_prima_id` int DEFAULT NULL,
  `produccion_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `detalle_compra_id` (`detalle_compra_id`),
  KEY `lote_produccion_id` (`lote_produccion_id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `merma_materia_prima_id` (`merma_materia_prima_id`),
  KEY `produccion_id` (`produccion_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `movimientos_materia_prima_ibfk_1` FOREIGN KEY (`detalle_compra_id`) REFERENCES `detalle_compra` (`id`),
  CONSTRAINT `movimientos_materia_prima_ibfk_2` FOREIGN KEY (`lote_produccion_id`) REFERENCES `lotes_produccion` (`id_lote`),
  CONSTRAINT `movimientos_materia_prima_ibfk_3` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `movimientos_materia_prima_ibfk_4` FOREIGN KEY (`merma_materia_prima_id`) REFERENCES `mermas_materia_prima` (`id`),
  CONSTRAINT `movimientos_materia_prima_ibfk_5` FOREIGN KEY (`produccion_id`) REFERENCES `produccion` (`id_produccion`),
  CONSTRAINT `movimientos_materia_prima_ibfk_6` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `movimientos_receta`
--

DROP TABLE IF EXISTS `movimientos_receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_receta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `cantidad` float NOT NULL,
  `fecha` datetime NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `movimientos_receta_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `movimientos_receta_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pedido_detalle`
--

DROP TABLE IF EXISTS `pedido_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `producto_venta_id` int NOT NULL,
  `cantidad_lotes` int NOT NULL,
  `total_unidades` float NOT NULL,
  `precio_unitario` float DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_venta_id` (`producto_venta_id`),
  CONSTRAINT `pedido_detalle_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_detalle_ibfk_2` FOREIGN KEY (`producto_venta_id`) REFERENCES `producto_venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pedido_produccion`
--

DROP TABLE IF EXISTS `pedido_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_produccion` (
  `id_pedido_produccion` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `id_produccion` int NOT NULL,
  PRIMARY KEY (`id_pedido_produccion`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_produccion` (`id_produccion`),
  CONSTRAINT `pedido_produccion_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_produccion_ibfk_2` FOREIGN KEY (`id_produccion`) REFERENCES `produccion` (`id_produccion`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `estado` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `total` float DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `presentaciones`
--

DROP TABLE IF EXISTS `presentaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presentaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `tipo_medida_id` int NOT NULL,
  `cantidad_equivalente` float NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `uso` varchar(20) NOT NULL DEFAULT 'comercial',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `tipo_medida_id` (`tipo_medida_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `presentaciones_ibfk_1` FOREIGN KEY (`tipo_medida_id`) REFERENCES `tipo_medida` (`id`),
  CONSTRAINT `presentaciones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `procesos_productivos`
--

DROP TABLE IF EXISTS `procesos_productivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procesos_productivos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `procesos_productivos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `procesos_receta`
--

DROP TABLE IF EXISTS `procesos_receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procesos_receta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int NOT NULL,
  `proceso_productivo_id` int NOT NULL,
  `tiempo_estimado` float NOT NULL,
  `orden` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proceso_productivo_id` (`proceso_productivo_id`),
  KEY `receta_id` (`receta_id`),
  CONSTRAINT `procesos_receta_ibfk_1` FOREIGN KEY (`proceso_productivo_id`) REFERENCES `procesos_productivos` (`id`),
  CONSTRAINT `procesos_receta_ibfk_2` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `produccion`
--

DROP TABLE IF EXISTS `produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion` (
  `id_produccion` int NOT NULL AUTO_INCREMENT,
  `id_receta` int NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `es_retail` tinyint(1) NOT NULL,
  `id_solicitud_compra` int DEFAULT NULL,
  PRIMARY KEY (`id_produccion`),
  KEY `id_receta` (`id_receta`),
  KEY `usuario_id` (`usuario_id`),
  KEY `id_solicitud_compra` (`id_solicitud_compra`),
  CONSTRAINT `produccion_ibfk_1` FOREIGN KEY (`id_receta`) REFERENCES `recetas` (`id`),
  CONSTRAINT `produccion_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `produccion_ibfk_3` FOREIGN KEY (`id_solicitud_compra`) REFERENCES `solicitud_compra` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_produccion_movimiento_insumos` AFTER INSERT ON `produccion` FOR EACH ROW BEGIN
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

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_update_produccion_estado_pedido` AFTER UPDATE ON `produccion` FOR EACH ROW BEGIN
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

                INSERT INTO detalle_venta (id_venta, id_producto_venta, cantidad, precio_unitario)
                SELECT v_venta_id,
                       producto_venta_id,
                       CAST(total_unidades AS SIGNED),
                       precio_unitario
                FROM pedido_detalle
                WHERE pedido_id = v_pedido_id;

                UPDATE venta
                SET total = (SELECT SUM(COALESCE(precio_unitario, 0) * cantidad) FROM detalle_venta WHERE id_venta = v_venta_id)
                WHERE id = v_venta_id;

            END IF;
        END IF;

    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `produccion_proceso`
--

DROP TABLE IF EXISTS `produccion_proceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion_proceso` (
  `id_produccion_proceso` int NOT NULL AUTO_INCREMENT,
  `id_produccion` int NOT NULL,
  `id_proceso` int NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `orden` int DEFAULT NULL,
  `tiempo_estimado` float DEFAULT NULL,
  PRIMARY KEY (`id_produccion_proceso`),
  KEY `id_proceso` (`id_proceso`),
  KEY `id_produccion` (`id_produccion`),
  CONSTRAINT `produccion_proceso_ibfk_1` FOREIGN KEY (`id_proceso`) REFERENCES `procesos_productivos` (`id`),
  CONSTRAINT `produccion_proceso_ibfk_2` FOREIGN KEY (`id_produccion`) REFERENCES `produccion` (`id_produccion`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_update_proceso_completar_produccion` AFTER UPDATE ON `produccion_proceso` FOR EACH ROW BEGIN

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
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `producto_venta`
--

DROP TABLE IF EXISTS `producto_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int NOT NULL,
  `presentacion_id` int NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text,
  `tipo` varchar(20) NOT NULL,
  `cantidad_unidades` int NOT NULL,
  `precio_venta` float NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `presentacion_id` (`presentacion_id`),
  KEY `receta_id` (`receta_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `producto_venta_ibfk_1` FOREIGN KEY (`presentacion_id`) REFERENCES `presentaciones` (`id`),
  CONSTRAINT `producto_venta_ibfk_2` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `producto_venta_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `proveedor_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `receta_detalle`
--

DROP TABLE IF EXISTS `receta_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `cantidad` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `receta_id` (`receta_id`),
  CONSTRAINT `receta_detalle_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `receta_detalle_ibfk_2` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text,
  `cantidad_producida` float NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `imagen` blob,
  `imagen_tipo` varchar(50) DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reserva_stock`
--

DROP TABLE IF EXISTS `reserva_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(128) NOT NULL,
  `producto_venta_id` int NOT NULL,
  `receta_id` int NOT NULL,
  `cantidad_packs` int NOT NULL,
  `cantidad_unidades` float NOT NULL,
  `expiry` datetime NOT NULL,
  `creado_en` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `producto_venta_id` (`producto_venta_id`),
  KEY `receta_id` (`receta_id`),
  KEY `ix_reserva_stock_session_id` (`session_id`),
  CONSTRAINT `reserva_stock_ibfk_1` FOREIGN KEY (`producto_venta_id`) REFERENCES `producto_venta` (`id`),
  CONSTRAINT `reserva_stock_ibfk_2` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(255) DEFAULT NULL,
  `data` blob,
  `expiry` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `solicitud_compra`
--

DROP TABLE IF EXISTS `solicitud_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitud_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia_prima_id` int NOT NULL,
  `cantidad` float NOT NULL,
  `origen` varchar(20) NOT NULL,
  `referencia_id` int DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `referencia_id` (`referencia_id`),
  CONSTRAINT `solicitud_compra_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `solicitud_compra_ibfk_2` FOREIGN KEY (`referencia_id`) REFERENCES `pedidos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_medida`
--

DROP TABLE IF EXISTS `tipo_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_medida` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `unidad_base` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unidad_medida`
--

DROP TABLE IF EXISTS `unidad_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidad_medida` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `abreviatura` varchar(10) NOT NULL,
  `tipo_medida_id` int NOT NULL,
  `valor_conversion` decimal(10,4) NOT NULL,
  `es_base_sistema` tinyint(1) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `abreviatura` (`abreviatura`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `tipo_medida_id` (`tipo_medida_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `unidad_medida_ibfk_1` FOREIGN KEY (`tipo_medida_id`) REFERENCES `tipo_medida` (`id`),
  CONSTRAINT `unidad_medida_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fs_uniquifier` varchar(255) NOT NULL,
  `reset_token` varchar(255) DEFAULT NULL,
  `reset_token_expiry` datetime DEFAULT NULL,
  `rol_id` int NOT NULL,
  `actualizado_por` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_pedido` int DEFAULT NULL,
  `fecha` datetime NOT NULL,
  `cancelada` tinyint(1) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `total` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_pedido` (`id_pedido`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `vw_costo_promedio_mp`
--

DROP TABLE IF EXISTS `vw_costo_promedio_mp`;
/*!50001 DROP VIEW IF EXISTS `vw_costo_promedio_mp`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_costo_promedio_mp` AS SELECT 
 1 AS `materia_prima_id`,
 1 AS `costo_promedio`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_costo_receta`
--

DROP TABLE IF EXISTS `vw_costo_receta`;
/*!50001 DROP VIEW IF EXISTS `vw_costo_receta`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_costo_receta` AS SELECT 
 1 AS `receta_id`,
 1 AS `nombre`,
 1 AS `costo_total`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_mermas_por_mes`
--

DROP TABLE IF EXISTS `vw_mermas_por_mes`;
/*!50001 DROP VIEW IF EXISTS `vw_mermas_por_mes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_mermas_por_mes` AS SELECT 
 1 AS `anio`,
 1 AS `mes`,
 1 AS `total_mermas_unidades`,
 1 AS `costo_total_mermas`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_top_producto_producido`
--

DROP TABLE IF EXISTS `vw_top_producto_producido`;
/*!50001 DROP VIEW IF EXISTS `vw_top_producto_producido`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_top_producto_producido` AS SELECT 
 1 AS `id`,
 1 AS `nombre`,
 1 AS `total_producido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_top_producto_vendido`
--

DROP TABLE IF EXISTS `vw_top_producto_vendido`;
/*!50001 DROP VIEW IF EXISTS `vw_top_producto_vendido`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_top_producto_vendido` AS SELECT 
 1 AS `id`,
 1 AS `nombre`,
 1 AS `total_vendido`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_utilidad_producto`
--

DROP TABLE IF EXISTS `vw_utilidad_producto`;
/*!50001 DROP VIEW IF EXISTS `vw_utilidad_producto`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_utilidad_producto` AS SELECT 
 1 AS `receta_id`,
 1 AS `nombre`,
 1 AS `costo_total`,
 1 AS `precio_venta`,
 1 AS `unidades_vendidas`,
 1 AS `ingresos`,
 1 AS `costo_total_vendido`,
 1 AS `utilidad`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ventas_por_mes`
--

DROP TABLE IF EXISTS `vw_ventas_por_mes`;
/*!50001 DROP VIEW IF EXISTS `vw_ventas_por_mes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ventas_por_mes` AS SELECT 
 1 AS `anio`,
 1 AS `mes`,
 1 AS `total_unidades_vendidas`,
 1 AS `total_pedidos`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ventas_receta`
--

DROP TABLE IF EXISTS `vw_ventas_receta`;
/*!50001 DROP VIEW IF EXISTS `vw_ventas_receta`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ventas_receta` AS SELECT 
 1 AS `receta_id`,
 1 AS `unidades_vendidas`,
 1 AS `precio_venta_promedio`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'cloud_brew'
--

--
-- Dumping routines for database 'cloud_brew'
--

--
-- Final view structure for view `vw_costo_promedio_mp`
--

/*!50001 DROP VIEW IF EXISTS `vw_costo_promedio_mp`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_costo_promedio_mp` AS select `dc`.`materia_prima_id` AS `materia_prima_id`,avg(`dc`.`precio_unitario`) AS `costo_promedio` from (`detalle_compra` `dc` join `compra` `c` on((`dc`.`compra_id` = `c`.`id`))) where ((`c`.`cancelada` = 0) and (`c`.`fecha_compra` >= (curdate() - interval 1 month))) group by `dc`.`materia_prima_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_costo_receta`
--

/*!50001 DROP VIEW IF EXISTS `vw_costo_receta`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_costo_receta` AS select `r`.`id` AS `receta_id`,`r`.`nombre` AS `nombre`,sum((`rd`.`cantidad` * ifnull(`v`.`costo_promedio`,0))) AS `costo_total` from ((`recetas` `r` join `receta_detalle` `rd` on((`r`.`id` = `rd`.`receta_id`))) left join `vw_costo_promedio_mp` `v` on((`rd`.`materia_prima_id` = `v`.`materia_prima_id`))) group by `r`.`id`,`r`.`nombre` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_mermas_por_mes`
--

/*!50001 DROP VIEW IF EXISTS `vw_mermas_por_mes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_mermas_por_mes` AS select year(`m`.`fecha_registro`) AS `anio`,month(`m`.`fecha_registro`) AS `mes`,sum(`m`.`cantidad`) AS `total_mermas_unidades`,round(sum((`m`.`cantidad` * coalesce((select `dc`.`precio_unitario` from `detalle_compra` `dc` where (`dc`.`materia_prima_id` = `m`.`materia_prima_id`) order by `dc`.`id` desc limit 1),0))),2) AS `costo_total_mermas` from `mermas_materia_prima` `m` where (`m`.`activo` = 1) group by `anio`,`mes` order by `anio` desc,`mes` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_top_producto_producido`
--

/*!50001 DROP VIEW IF EXISTS `vw_top_producto_producido`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_top_producto_producido` AS select `r`.`id` AS `id`,`r`.`nombre` AS `nombre`,sum(`p`.`cantidad`) AS `total_producido` from (`produccion` `p` join `recetas` `r` on((`r`.`id` = `p`.`id_receta`))) group by `r`.`id`,`r`.`nombre` order by `total_producido` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_top_producto_vendido`
--

/*!50001 DROP VIEW IF EXISTS `vw_top_producto_vendido`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_top_producto_vendido` AS select `r`.`id` AS `id`,`r`.`nombre` AS `nombre`,sum(`pd`.`total_unidades`) AS `total_vendido` from ((`pedido_detalle` `pd` join `producto_venta` `pv` on((`pv`.`id` = `pd`.`producto_venta_id`))) join `recetas` `r` on((`r`.`id` = `pv`.`receta_id`))) group by `r`.`id`,`r`.`nombre` order by `total_vendido` desc limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_utilidad_producto`
--

/*!50001 DROP VIEW IF EXISTS `vw_utilidad_producto`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_utilidad_producto` AS select `r`.`receta_id` AS `receta_id`,`r`.`nombre` AS `nombre`,`r`.`costo_total` AS `costo_total`,ifnull(`v`.`precio_venta_promedio`,0) AS `precio_venta`,`v`.`unidades_vendidas` AS `unidades_vendidas`,(`v`.`unidades_vendidas` * ifnull(`v`.`precio_venta_promedio`,0)) AS `ingresos`,(`v`.`unidades_vendidas` * `r`.`costo_total`) AS `costo_total_vendido`,((`v`.`unidades_vendidas` * ifnull(`v`.`precio_venta_promedio`,0)) - (`v`.`unidades_vendidas` * `r`.`costo_total`)) AS `utilidad` from (`vw_costo_receta` `r` left join `vw_ventas_receta` `v` on((`r`.`receta_id` = `v`.`receta_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ventas_por_mes`
--

/*!50001 DROP VIEW IF EXISTS `vw_ventas_por_mes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_ventas_por_mes` AS select year(`p`.`fecha_registro`) AS `anio`,month(`p`.`fecha_registro`) AS `mes`,sum(`pd`.`total_unidades`) AS `total_unidades_vendidas`,count(distinct `p`.`id`) AS `total_pedidos` from (`pedidos` `p` join `pedido_detalle` `pd` on((`pd`.`pedido_id` = `p`.`id`))) where (`p`.`activo` = 1) group by `anio`,`mes` order by `anio` desc,`mes` desc limit 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ventas_receta`
--

/*!50001 DROP VIEW IF EXISTS `vw_ventas_receta`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_ventas_receta` AS select `pv`.`receta_id` AS `receta_id`,sum(`pd`.`total_unidades`) AS `unidades_vendidas`,avg(`pv`.`precio_venta`) AS `precio_venta_promedio` from ((`pedido_detalle` `pd` join `producto_venta` `pv` on((`pv`.`id` = `pd`.`producto_venta_id`))) join `pedidos` `p` on((`pd`.`pedido_id` = `p`.`id`))) where (`p`.`activo` = 1) group by `pv`.`receta_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-15 16:03:27
