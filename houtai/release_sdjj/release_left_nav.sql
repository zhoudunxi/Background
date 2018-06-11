-- MySQL dump 10.14  Distrib 5.5.56-MariaDB, for Linux (x86_64)
--
-- Host: 192.168.30.133    Database: release_sdjj
-- ------------------------------------------------------
-- Server version	5.6.29-76.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `release_left_nav`
--

DROP TABLE IF EXISTS `release_left_nav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `release_left_nav` (
  `left_navid` int(11) NOT NULL AUTO_INCREMENT,
  `left_nav_pid` int(11) NOT NULL,
  `left_nav_title` varchar(50) NOT NULL,
  `left_nav_url` varchar(240) NOT NULL,
  `left_nav_sort` int(11) NOT NULL,
  PRIMARY KEY (`left_navid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `release_left_nav`
--

LOCK TABLES `release_left_nav` WRITE;
/*!40000 ALTER TABLE `release_left_nav` DISABLE KEYS */;
INSERT INTO `release_left_nav` VALUES (2,1,'代码提交','/release',0),(3,1,'请求列表','/requestlist',1),(4,1,'项目管理','/projectmanegement',2),(5,1,'设置','/setting',99),(6,1,'帮助','/help',100),(7,1,'更新APK','/apkupdate',3),(8,1,'APK队列','/apkupdate/apkqueue',4),(9,1,'资产管理','/cmdb',5);
/*!40000 ALTER TABLE `release_left_nav` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-15 14:30:35
