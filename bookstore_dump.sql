/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.10-MariaDB, for Linux (aarch64)
--
-- Host: localhost    Database: Bookstore
-- ------------------------------------------------------
-- Server version	11.4.10-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `birth_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `bio_text` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` VALUES
(1,'Сорокин','Владимир','1995-08-07 00:00:00','Русский писатель, сценарист и драматург, родился в подмосковном посёлке Быково в семье профессора и экономиста. С детства увлекался рисованием, окончил Московский нефтяной институт, где получил специальность инженера-механика, но по профессии почти не работал. Начал публиковаться в самиздате в конце 1970-х годов, а в 1990-е годы стал одним из самых заметных и скандальных авторов современной русской литературы.'),
(2,'Харрис','Роберт','1957-03-07 00:00:00','нглийский писатель и журналист, родился в Ноттингеме в семье печатника. Окончил Селвин-колледж в Кембридже. Работал на BBC, был политическим редактором газет The Observer, The Sunday Times и The Daily Telegraph. Его первый роман «Фатерланд» (альтернативная история о победе нацистской Германии) мгновенно стал международным бестселлером. '),
(3,'Стюарт','Джеймс Б.','1951-02-28 00:00:00','мериканский экономист, профессор Пенсильванского университета. Специализируется в области трудовых отношений, афроамериканских исследований и менеджмента. В 2021 году получил высшую награду Национальной экономической ассоциации США — премию Сэмюэля Вестерфилда'),
(4,'Хмелевская','Иона','1932-04-02 00:00:00','Польская писательница, «королева иронического детектива», родилась в Варшаве в семье директора банка. Окончила архитектурный факультет Варшавского политехнического института, работала архитектором-проектировщиком, но прославилась как писательница. Первый рассказ опубликовала в 1958 году, а первый роман «Клин клином» — в 1964 году. '),
(6,'Чемберс','Клэр','1966-01-19 00:00:00','Британская писательница, родилась в Кройдоне (Южный Лондон). Изучала английскую литературу в Оксфордском университете . После окончания университета год жила в Новой Зеландии, где написала свой первый роман. Начала карьеру в издательстве André Deutsch, где работала редактором, а затем полностью сосредоточилась на писательской карьере '),
(7,'Хилслоп','Виктория','1959-06-08 00:00:00','Английская писательница, родилась в Бромли (графство Кент). Изучала английский язык в колледже Святой Хильды Оксфордского университета . Работала в издательском деле и журналистике, писала заметки о путешествиях для Sunday Telegraph и других изданий . Всемирную известность ей принёс второй роман «Остров» (The Island, 2005) — бестселлер номер один в Великобритании, действие которого происходит на Крите и острове Спиналонга'),
(8,'Шодерло де Лакло','Пьер','1741-10-18 00:00:00','Французский военачальник, политик, изобретатель и писатель, родился в Амьене в семье небогатых дворян. Получил образование артиллериста, дослужился до генеральского чина. Был секретарём герцога Орлеанского, членом якобинского клуба.');
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `book_id` int(10) unsigned NOT NULL,
  `genre_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `book_genre_genres_FK` (`genre_id`),
  CONSTRAINT `book_genre_books_FK` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `book_genre_genres_FK` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES
(1,1),
(2,2),
(3,2),
(4,3),
(5,3),
(6,3),
(9,5),
(7,6),
(8,6),
(10,6);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `publication_year` int(10) unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT 0.00,
  `stock_quantity` int(11) NOT NULL,
  `author_id` int(10) unsigned DEFAULT NULL,
  `publisher_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `books_unique` (`isbn`),
  KEY `books_title_IDX` (`title`) USING BTREE,
  KEY `books_isbn_IDX` (`isbn`) USING BTREE,
  KEY `books_authors_FK` (`author_id`),
  KEY `books_publisher_FK` (`publisher_id`),
  CONSTRAINT `books_authors_FK` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `books_publisher_FK` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES
(1,'Теллурия','978-5-17-080466-5',2013,550.00,49,1,1),
(2,'Шайка воров с Уолл-стрит','978-5-9614-5152-8',2015,890.00,80,3,2),
(3,'Фатерланд','978-5-389-24182-4',2023,350.00,75,2,3),
(4,'Всё красное','978-5-907500-09-9 ',2022,750.00,46,4,4),
(5,'Проселочные дороги','5-86471-017-2 ',1994,690.00,84,4,5),
(6,'Колодцы предков','978-5-907500-18-1',2022,1200.00,35,4,4),
(7,'Возвращение','978-5-389-17121-3',2020,1150.00,20,7,7),
(8,'Робкие создания','978-5-17-168198-2',2025,670.00,19,6,1),
(9,'Опасные связи','978-5-699-78755-5',2015,240.00,68,8,6),
(10,'Элли и арфист','978-5-17-167658-2',2025,560.00,2,7,1);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `customers_email_IDX` (`email`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES
(1,'Сказкина','Елена','bu@mail.ru','7897895478','2026-05-21 11:54:21','2026-06-03 13:04:49'),
(2,'Романова','Алина','alin@gmail.com','+78956425898','2026-06-03 13:04:49','2026-06-03 13:04:49'),
(3,'Прозов','Николай','prozza@gmail.com','+78956523256','2026-06-03 13:06:21','2026-06-03 13:06:21');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`%`*/ /*!50003 TRIGGER update_updated_at
BEFORE UPDATE ON customers
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES
(1,'Роман-антиутопия'),
(2,'Триллер'),
(3,'Детектив'),
(4,'Мистика'),
(5,'Эпистолярный роман'),
(6,' Роман');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` int(10) unsigned NOT NULL,
  `book_id` int(10) unsigned NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`),
  KEY `order_items_orders_FK` (`order_id`),
  KEY `order_items_books_FK` (`book_id`),
  CONSTRAINT `order_items_books_FK` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `order_items_orders_FK` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `customer_id` int(10) unsigned NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` enum('pending','confirmed','shipped','delivered','cancelled') NOT NULL DEFAULT 'pending',
  `total_price` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id`),
  KEY `orders_customers_FK` (`customer_id`),
  CONSTRAINT `orders_customers_FK` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publisher`
--

DROP TABLE IF EXISTS `publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `publisher` (
  `name` varchar(100) NOT NULL,
  `country` varchar(50) NOT NULL,
  `founded_year` int(11) NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publisher`
--

LOCK TABLES `publisher` WRITE;
/*!40000 ALTER TABLE `publisher` DISABLE KEYS */;
INSERT INTO `publisher` VALUES
('CORPUS/ACT','Россия',2008,1),
('Альпина Паблишер','Россия',1998,2),
('Иностранка','Россия',2000,3),
('Аркадия','Россия',2017,4),
('Фантом Пресс','Россия',1992,5),
('Эксмо','Россия',1991,6),
('Азбука','Россия',1995,7);
/*!40000 ALTER TABLE `publisher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-06-29 22:08:52
