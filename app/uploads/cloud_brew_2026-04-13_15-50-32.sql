-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: cloud_brew
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('f1ea2756ddc1');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora_login`
--

LOCK TABLES `bitacora_login` WRITE;
/*!40000 ALTER TABLE `bitacora_login` DISABLE KEYS */;
INSERT INTO `bitacora_login` VALUES (1,'2026-04-12','2026-04-12 01:54:00','test@test.com',1,'Login correcto'),(2,'2026-04-12','2026-04-12 10:17:50','test@test.com',1,'Login correcto'),(3,'2026-04-12','2026-04-12 12:43:36','test@test.com',0,'Error en captaci√≥n de Captcha'),(4,'2026-04-12','2026-04-12 12:43:45','test@test.com',1,'Login correcto'),(5,'2026-04-12','2026-04-12 13:31:23','test@test.com',1,'Login correcto'),(6,'2026-04-12','2026-04-12 16:51:24','test@test.com',1,'Login correcto'),(7,'2026-04-12','2026-04-12 20:38:54','test@test.com',0,'Error en captaci√≥n de Captcha'),(8,'2026-04-12','2026-04-12 20:39:07','test@test.com',1,'Login correcto'),(9,'2026-04-12','2026-04-12 20:45:04','test@test.com',1,'Login correcto'),(10,'2026-04-12','2026-04-12 20:46:13','test@test.com',1,'Login correcto'),(11,'2026-04-13','2026-04-13 15:43:08','test@test.com',1,'Login correcto');
/*!40000 ALTER TABLE `bitacora_login` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Manuel','Hernandez','manuelmhernandez37@gmail.com','','CALLE','COLONIA','LEON','ESTADO','34567','retail','2026-04-12 07:58:50',1,1);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra`
--

LOCK TABLES `compra` WRITE;
/*!40000 ALTER TABLE `compra` DISABLE KEYS */;
INSERT INTO `compra` VALUES (1,'2026-04-12 01:55:48','2026-04-12 01:55:57',0,1,1,'Usuario de Prueba'),(2,'2026-04-12 19:12:21','2026-04-12 19:12:30',0,1,1,'Usuario de Prueba');
/*!40000 ALTER TABLE `compra` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compra`
--

LOCK TABLES `detalle_compra` WRITE;
/*!40000 ALTER TABLE `detalle_compra` DISABLE KEYS */;
INSERT INTO `detalle_compra` VALUES (1,1,1,1,5,30),(2,2,1,1,40,100);
/*!40000 ALTER TABLE `detalle_compra` ENABLE KEYS */;
UNLOCK TABLES;
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
  `id_receta` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` float DEFAULT NULL,
  `subtotal` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_receta` (`id_receta`),
  KEY `id_venta` (`id_venta`),
  CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_receta`) REFERENCES `recetas` (`id`),
  CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_venta`
--

LOCK TABLES `detalle_venta` WRITE;
/*!40000 ALTER TABLE `detalle_venta` DISABLE KEYS */;
INSERT INTO `detalle_venta` VALUES (1,1,1,2,20,40);
/*!40000 ALTER TABLE `detalle_venta` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lotes_produccion`
--

LOCK TABLES `lotes_produccion` WRITE;
/*!40000 ALTER TABLE `lotes_produccion` DISABLE KEYS */;
INSERT INTO `lotes_produccion` VALUES (1,1,'12.04.2026.01.April','2026-04-12',2),(2,2,'12.04.2026.02.April','2026-04-12',2);
/*!40000 ALTER TABLE `lotes_produccion` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_lote_movimiento_receta` AFTER INSERT ON `lotes_produccion` FOR EACH ROW BEGIN
    DECLARE v_receta_id INT;
    DECLARE v_usuario_id INT;

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
        CONCAT('Entrada por completaci√≥n de Producci√≥n #', NEW.id_produccion, ' - Lote ', NEW.codigo_lote),
        v_usuario_id
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
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_lote_entrada_receta` AFTER INSERT ON `lotes_produccion` FOR EACH ROW BEGIN
    DECLARE v_receta_id INT;
    DECLARE v_usuario_id INT;

    -- 1. Identificamos la receta y el usuario desde la tabla produccion/compra
    -- Nota: Como 'produccion' no tiene usuario_id, usamos uno por defecto o el de la sesi√≥n
    SELECT p.id_receta INTO v_receta_id
    FROM produccion p
    WHERE p.id_produccion = NEW.id_produccion;

    -- 2. Insertamos la entrada en movimientos_receta (que es tu tabla para productos terminados)
    IF v_receta_id IS NOT NULL THEN
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
            CONCAT('Entrada por Lote Finalizado #', NEW.codigo_lote),
            1 -- ID de usuario administrador o responsable por defecto
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
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (1,'Malta clara','MALTA CLARA DE CEBADA',1,100,1,1),(2,'Agua','',2,1000,1,1);
/*!40000 ALTER TABLE `materias_primas` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mermas_materia_prima`
--

LOCK TABLES `mermas_materia_prima` WRITE;
/*!40000 ALTER TABLE `mermas_materia_prima` DISABLE KEYS */;
INSERT INTO `mermas_materia_prima` VALUES (1,1,30,'Caida','2026-04-12 16:26:28',1,1),(2,1,200,'CAIDA','2026-04-13 00:49:40',1,1);
/*!40000 ALTER TABLE `mermas_materia_prima` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
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
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_materia_prima`
--

LOCK TABLES `movimientos_materia_prima` WRITE;
/*!40000 ALTER TABLE `movimientos_materia_prima` DISABLE KEYS */;
INSERT INTO `movimientos_materia_prima` VALUES (1,1,'entrada',250,'2026-04-12 01:55:57','Compra #1 - Detalle #1',1,1,NULL,NULL,NULL),(2,1,'salida',10,'2026-04-12 01:58:09','Salida por inicio de Producci√≥n #1',1,NULL,NULL,NULL,1),(3,1,'salida',10,'2026-04-12 02:00:06','Salida por inicio de Producci√≥n #2',1,NULL,NULL,NULL,2),(4,1,'salida',30,'2026-04-12 10:26:27','Merma #1: Caida',1,NULL,NULL,1,NULL),(5,1,'salida',200,'2026-04-12 18:49:40','Merma #2: CAIDA',1,NULL,NULL,2,NULL),(6,1,'entrada',2000,'2026-04-12 19:12:30','Compra #2 - Detalle #2',1,2,NULL,NULL,NULL),(7,1,'salida',100,'2026-04-12 19:14:15','Salida por inicio de Producci√≥n #3',1,NULL,NULL,NULL,3);
/*!40000 ALTER TABLE `movimientos_materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_receta`
--

LOCK TABLES `movimientos_receta` WRITE;
/*!40000 ALTER TABLE `movimientos_receta` DISABLE KEYS */;
INSERT INTO `movimientos_receta` VALUES (1,1,'entrada',2,'2026-04-12 01:58:13','Entrada por completaci√≥n de Producci√≥n #1 - Lote 12.04.2026.01.April',1),(2,1,'entrada',2,'2026-04-12 01:58:13','Entrada por Lote Finalizado #12.04.2026.01.April',1),(3,1,'entrada',2,'2026-04-12 02:00:23','Entrada por completaci√≥n de Producci√≥n #2 - Lote 12.04.2026.02.April',1),(4,1,'entrada',2,'2026-04-12 02:00:23','Entrada por Lote Finalizado #12.04.2026.02.April',1);
/*!40000 ALTER TABLE `movimientos_receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_detalle`
--

DROP TABLE IF EXISTS `pedido_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `receta_id` int NOT NULL,
  `cantidad_lotes` int NOT NULL,
  `total_unidades` float NOT NULL,
  `precio_unitario` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `receta_id` (`receta_id`),
  CONSTRAINT `pedido_detalle_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  CONSTRAINT `pedido_detalle_ibfk_2` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_detalle`
--

LOCK TABLES `pedido_detalle` WRITE;
/*!40000 ALTER TABLE `pedido_detalle` DISABLE KEYS */;
INSERT INTO `pedido_detalle` VALUES (1,1,1,1,2,20),(7,5,3,2,4,NULL);
/*!40000 ALTER TABLE `pedido_detalle` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_produccion`
--

LOCK TABLES `pedido_produccion` WRITE;
/*!40000 ALTER TABLE `pedido_produccion` DISABLE KEYS */;
INSERT INTO `pedido_produccion` VALUES (1,1,2),(2,5,3);
/*!40000 ALTER TABLE `pedido_produccion` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,1,'2026-04-12 08:00:06','Terminado',1,40,1),(5,1,'2026-04-13 01:14:15','Pendiente',1,50,1);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `tipo_medida_id` (`tipo_medida_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `presentaciones_ibfk_1` FOREIGN KEY (`tipo_medida_id`) REFERENCES `tipo_medida` (`id`),
  CONSTRAINT `presentaciones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presentaciones`
--

LOCK TABLES `presentaciones` WRITE;
/*!40000 ALTER TABLE `presentaciones` DISABLE KEYS */;
INSERT INTO `presentaciones` VALUES (1,'Bulto',1,50,1,1),(2,'Kilo',1,100,1,1),(3,'A',1,20,0,1),(4,'Litro',2,1,1,1);
/*!40000 ALTER TABLE `presentaciones` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procesos_productivos`
--

LOCK TABLES `procesos_productivos` WRITE;
/*!40000 ALTER TABLE `procesos_productivos` DISABLE KEYS */;
INSERT INTO `procesos_productivos` VALUES (1,'FERMENTACION','Maceracion y fermentacion',1,1);
/*!40000 ALTER TABLE `procesos_productivos` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procesos_receta`
--

LOCK TABLES `procesos_receta` WRITE;
/*!40000 ALTER TABLE `procesos_receta` DISABLE KEYS */;
INSERT INTO `procesos_receta` VALUES (6,3,1,60,1),(7,2,1,50,1),(8,1,1,60,1);
/*!40000 ALTER TABLE `procesos_receta` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`id_produccion`),
  KEY `id_receta` (`id_receta`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `produccion_ibfk_1` FOREIGN KEY (`id_receta`) REFERENCES `recetas` (`id`),
  CONSTRAINT `produccion_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion`
--

LOCK TABLES `produccion` WRITE;
/*!40000 ALTER TABLE `produccion` DISABLE KEYS */;
INSERT INTO `produccion` VALUES (1,1,'2026-04-12','2026-04-12','en proceso',1,1),(2,1,'2026-04-12','2026-04-12','en proceso',1,1),(3,3,NULL,NULL,'pendiente',1,1);
/*!40000 ALTER TABLE `produccion` ENABLE KEYS */;
UNLOCK TABLES;
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
        SET MESSAGE_TEXT = 'Error: La receta no tiene ingredientes configurados. No se puede registrar la producci√≥n.';
    END IF;

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
        CONCAT('Salida por inicio de Producci√≥n #', NEW.id_produccion),
        v_usuario_id,
        NEW.id_produccion
    FROM receta_detalle rd
    WHERE rd.receta_id = NEW.id_receta;

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

                INSERT INTO detalle_venta (id_venta, id_receta, cantidad, precio_unitario, subtotal)
                SELECT v_venta_id,
                       receta_id,
                       CAST(total_unidades AS SIGNED),
                       precio_unitario,
                       CAST(total_unidades AS SIGNED) * COALESCE(precio_unitario, 0)
                FROM pedido_detalle
                WHERE pedido_id = v_pedido_id;

                UPDATE venta
                SET total = (SELECT SUM(subtotal) FROM detalle_venta WHERE id_venta = v_venta_id)
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_proceso`
--

LOCK TABLES `produccion_proceso` WRITE;
/*!40000 ALTER TABLE `produccion_proceso` DISABLE KEYS */;
INSERT INTO `produccion_proceso` VALUES (1,1,1,NULL,NULL,'completado',1,60),(2,2,1,NULL,NULL,'completado',1,60),(3,3,1,NULL,NULL,'pendiente',1,60);
/*!40000 ALTER TABLE `produccion_proceso` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
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
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'PROVEEDOR','3456778980','manuelmhernandez37@gmail.com','DIRECCION-3',1,1);
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_detalle`
--

LOCK TABLES `receta_detalle` WRITE;
/*!40000 ALTER TABLE `receta_detalle` DISABLE KEYS */;
INSERT INTO `receta_detalle` VALUES (8,3,1,100),(9,2,1,500),(10,2,2,1),(11,1,1,10);
/*!40000 ALTER TABLE `receta_detalle` ENABLE KEYS */;
UNLOCK TABLES;

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
  `precio_venta` float DEFAULT NULL,
  `imagen` blob,
  `imagen_tipo` varchar(50) DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,'Lager cantidad producida  20','Lager suave',2,1,25,NULL,NULL,1),(2,'Koppf','Lager suave',2,1,25,NULL,NULL,1),(3,'Malta season','Lager suave',2,1,25,NULL,NULL,1);
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'admin','Administrador del sistema');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
INSERT INTO `session` VALUES (1,'session:hor4AqdFpTCMLOen1Rzq2TY0a_9-lLKZmXA4UDfu6bw',_binary 'ä™_permanent√™csrf_token\Ÿ(c9dfbaa87f84f631838ce63d57dbae570d997815¶_fresh√®_user_id°1£_idŸÄ27d449ef089f2c5cfd97f53692f9b7f799ebccd87b091f5e7f00a575bcbc70a3e2674b2c49cc54781d1d9dbc8523e4ef0a442a115eac49f7bd675eeeed2a6d6dÆcompra_carritoê∑receta_carrito_detallesê∑receta_carrito_procesosêØpedido_detallesëÑ©receta_id≠receta_nombreºLager cantidad producida  20Æcantidad_lotesÆtotal_unidades\À@\0\0\0\0\0\0\0≤editando_pedido_id','2026-04-12 08:31:00'),(2,'session:gPLp73xjmMpiyWDdQHPTmHWE-srRF3CZQKNQC_2KQUU',_binary 'Ö™_permanent√™csrf_token\Ÿ(c22cb8d23c926da730b0a75d95123444a56665a9¶_fresh√®_user_id°1£_idŸÄ27d449ef089f2c5cfd97f53692f9b7f799ebccd87b091f5e7f00a575bcbc70a3e2674b2c49cc54781d1d9dbc8523e4ef0a442a115eac49f7bd675eeeed2a6d6d','2026-04-12 17:51:34'),(3,'session:u_OPwBL-pv8QVkunVNmyF-_V5tUPmWQMdPkomSbXDmc',_binary 'Ö™_permanent√™csrf_token\Ÿ(f1c2c26035e52f398ad03ff2811b03fed1940eca¶_fresh√®_user_id°1£_idŸÄ27d449ef089f2c5cfd97f53692f9b7f799ebccd87b091f5e7f00a575bcbc70a3e2674b2c49cc54781d1d9dbc8523e4ef0a442a115eac49f7bd675eeeed2a6d6d','2026-04-12 19:15:19'),(4,'session:2Et88RIIAYV4p0A-DMfglMoPKnhhBzxsuvvv3Bacru0',_binary 'Ñ™_permanent√™csrf_token\Ÿ(12795d7b4d180cd98e535e7b4e12148c1c9b8543¶_fresh¬Æcaptcha_answer•86640','2026-04-12 19:15:26'),(5,'session:4xC2VwvpRg_pzRQw26c5GKPBMg9wv44jzKVO79nxOAg',_binary 'à™_permanent√™csrf_token\Ÿ(8d3b49ef5615e9c8ee826068c8b339205146176d¶_fresh√®_user_id°1£_idŸÄ27d449ef089f2c5cfd97f53692f9b7f799ebccd87b091f5e7f00a575bcbc70a3e2674b2c49cc54781d1d9dbc8523e4ef0a442a115eac49f7bd675eeeed2a6d6dÆcompra_carritoê∑receta_carrito_detallesê∑receta_carrito_procesosê','2026-04-12 22:44:05'),(6,'session:xcTX1Nc6nPxsZqqBFjsc9RK9SgldkwbAxq3TN9MV0AE',_binary 'ä™_permanent√™csrf_token\Ÿ(043432ca1e08a423ab1fe49017d9960add130183¶_fresh√®_user_id°1£_idŸÄ27d449ef089f2c5cfd97f53692f9b7f799ebccd87b091f5e7f00a575bcbc70a3e2674b2c49cc54781d1d9dbc8523e4ef0a442a115eac49f7bd675eeeed2a6d6d∫receta_carrito_editando_id∑receta_carrito_detallesê∑receta_carrito_procesosêØpedido_detallesêÆcompra_carritoê','2026-04-13 01:55:09'),(7,'session:3YA2znvSOddy5-v4LcQtJ_QMvW1gIjN0a9XtYBIJNpU',_binary 'Ñ™_permanent√™csrf_token\Ÿ(4fab3c7a8ae08a6da9eab56a9f2b3202214c425f¶_fresh¬Æcaptcha_answer•42507','2026-04-13 03:16:30'),(8,'session:XuQj6vRD6FO9k--LtGHRd4IpM3imRkfuLA6rPqEvWtg',_binary 'Ö™_permanent√™csrf_token\Ÿ(13f26564dd2abb670a4ca0652136ad9228efe92a¶_fresh√®_user_id°1£_idŸÄ27d449ef089f2c5cfd97f53692f9b7f799ebccd87b091f5e7f00a575bcbc70a3e2674b2c49cc54781d1d9dbc8523e4ef0a442a115eac49f7bd675eeeed2a6d6d','2026-04-13 22:20:29');
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `tipo_medida`
--

LOCK TABLES `tipo_medida` WRITE;
/*!40000 ALTER TABLE `tipo_medida` DISABLE KEYS */;
INSERT INTO `tipo_medida` VALUES (1,'Masa','Gramos'),(2,'Volumen','Litros'),(3,'Pieza','Piezas');
/*!40000 ALTER TABLE `tipo_medida` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidad_medida`
--

LOCK TABLES `unidad_medida` WRITE;
/*!40000 ALTER TABLE `unidad_medida` DISABLE KEYS */;
INSERT INTO `unidad_medida` VALUES (1,'Gramos','g',1,1.0000,1,1,NULL),(2,'Litros','L',2,1.0000,1,1,NULL),(3,'Piezas','pz',3,1.0000,1,1,NULL),(4,'KILO','KG',1,100.0000,0,1,1);
/*!40000 ALTER TABLE `unidad_medida` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Usuario de Prueba','test@test.com','scrypt:32768:8:1$SWfsYiZqqshtp3iM$3ea6fe109ff13b3df8faa3e1a884cece88f81f437bda55576939db833b5917cb505a9d8fde3a7a748b2370aac3d775d7a75230537af0dd54ac0b850473b379e5',1,'303ed328f8f2499dbe457053c1e89586',NULL,NULL,1,NULL),(2,'TESTER','manuelmhernandez@gmail.com','scrypt:32768:8:1$542KxQ4BhcNuTyz2$0881fd3429924a57fe50223d68d761ce832e617170d95eb7c9b03af463c359e2a9217941a805bfb6c78c0506c76e5c71f13915637f26c78d5be780a914c38479',1,'a400bf4e42c3491b8f17eb1f87aaacbd',NULL,NULL,1,'Usuario de Prueba');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,1,1,'2026-04-12 02:00:23',0,'retail',40);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vw_mermas_por_mes`
--

DROP TABLE IF EXISTS `vw_mermas_por_mes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vw_mermas_por_mes` (
  `anio` int NOT NULL,
  `mes` int NOT NULL,
  `total_mermas_unidades` float DEFAULT NULL,
  `costo_total_mermas` float DEFAULT NULL,
  PRIMARY KEY (`anio`,`mes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vw_mermas_por_mes`
--

LOCK TABLES `vw_mermas_por_mes` WRITE;
/*!40000 ALTER TABLE `vw_mermas_por_mes` DISABLE KEYS */;
/*!40000 ALTER TABLE `vw_mermas_por_mes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vw_top_producto_producido`
--

DROP TABLE IF EXISTS `vw_top_producto_producido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vw_top_producto_producido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `total_producido` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vw_top_producto_producido`
--

LOCK TABLES `vw_top_producto_producido` WRITE;
/*!40000 ALTER TABLE `vw_top_producto_producido` DISABLE KEYS */;
/*!40000 ALTER TABLE `vw_top_producto_producido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vw_top_producto_vendido`
--

DROP TABLE IF EXISTS `vw_top_producto_vendido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vw_top_producto_vendido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `total_vendido` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vw_top_producto_vendido`
--

LOCK TABLES `vw_top_producto_vendido` WRITE;
/*!40000 ALTER TABLE `vw_top_producto_vendido` DISABLE KEYS */;
/*!40000 ALTER TABLE `vw_top_producto_vendido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vw_ventas_por_mes`
--

DROP TABLE IF EXISTS `vw_ventas_por_mes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vw_ventas_por_mes` (
  `anio` int NOT NULL,
  `mes` int NOT NULL,
  `total_unidades_vendidas` float DEFAULT NULL,
  `total_pedidos` int DEFAULT NULL,
  PRIMARY KEY (`anio`,`mes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vw_ventas_por_mes`
--

LOCK TABLES `vw_ventas_por_mes` WRITE;
/*!40000 ALTER TABLE `vw_ventas_por_mes` DISABLE KEYS */;
/*!40000 ALTER TABLE `vw_ventas_por_mes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'cloud_brew'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 15:50:33
