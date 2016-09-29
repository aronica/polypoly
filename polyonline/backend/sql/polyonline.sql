-- MySQL dump 10.13  Distrib 5.7.12, for Linux (x86_64)
--
-- Host: localhost    Database: polyonline
-- ------------------------------------------------------
-- Server version	5.7.12

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
-- Current Database: `polyonline`
--

/*!40000 DROP DATABASE IF EXISTS `polyonline`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `polyonline` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `polyonline`;

--
-- Table structure for table `comments`
--
DROP TABLE IF EXISTS `banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position` char(10) DEFAULT NULL,
  `shown` tinyint(1) DEFAULT '1',
  `sequence` int(11),
  `image` varchar(50),
  `link` varchar(1000),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `openid` varchar(64) DEFAULT NULL,
  `unionid` varchar(64) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `phone` char(11) DEFAULT NULL,
  `property_id` int(11) DEFAULT NULL,
  `structure_id` int(11) NOT NULL,
  `hall_score` int(11) DEFAULT NULL,
  `hall_comment` varchar(1000) DEFAULT NULL,
  `kitchen_score` int(11) DEFAULT NULL,
  `kitchen_comment` varchar(1000) DEFAULT NULL,
  `bedroom_score` int(11) DEFAULT NULL,
  `bedroom_comment` varchar(1000) DEFAULT NULL,
  `toilet_score` int(11) DEFAULT NULL,
  `toilet_comment` varchar(1000) DEFAULT NULL,
  `overview_score` int(11) DEFAULT NULL,
  `overview_comment` varchar(1000) DEFAULT NULL,
  `estimated_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `unionid` (`unionid`),
  KEY `openid` (`openid`),
  KEY `property_id` (`property_id`),
  KEY `structure_id` (`structure_id`),
  KEY `ix_ts` (`ts`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`unionid`) REFERENCES `weixin_profile` (`unionid`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `property` (`id`),
  CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`structure_id`) REFERENCES `structure` (`id`),
  CONSTRAINT `comments_ibfk_4` FOREIGN KEY (`openid`) REFERENCES `weixin_profile` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `city` varchar(10) DEFAULT NULL,
  `image` json DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `open_time_from` timestamp NULL DEFAULT NULL,
  `open_time_to` timestamp NULL DEFAULT NULL,
  `property_age` int(11) DEFAULT NULL,
  `surrounding` json DEFAULT NULL,
  `shown` tinyint(1) DEFAULT '1',
  `isnew` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_city` (`city`, `name`),
  KEY `ix_shown` (`shown`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `property_structure`
--

DROP TABLE IF EXISTS `property_structure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `property_structure` (
  `property_id` int(11) NOT NULL,
  `structure_id` int(11) NOT NULL,
  PRIMARY KEY (`property_id`,`structure_id`),
  KEY `structure_id` (`structure_id`),
  CONSTRAINT `property_structure_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `property` (`id`),
  CONSTRAINT `property_structure_ibfk_2` FOREIGN KEY (`structure_id`) REFERENCES `structure` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `structure`
--

DROP TABLE IF EXISTS `structure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `structure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL,
  `area` int(11) DEFAULT NULL,
  `room_count` int(11) DEFAULT NULL,
  `hall_count` int(11) DEFAULT NULL,
  `toilet_count` int(11) DEFAULT NULL,
  `lowest_price` int(11) DEFAULT NULL,
  `hall_image` varchar(50) DEFAULT NULL,
  `kitchen_image` varchar(50) DEFAULT NULL,
  `bedroom_image` varchar(50) DEFAULT NULL,
  `toilet_image` varchar(50) DEFAULT NULL,
  `position_image` varchar(50) DEFAULT NULL,
  `shown` tinyint(1) DEFAULT '1',
  `sketchfab_id` varchar(50) DEFAULT NULL,
  `720yun_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_name` (`name`),
  KEY `ix_area` (`area`),
  KEY `ix_room` (`room_count`),
  KEY `ix_hall` (`hall_count`),
  KEY `ix_toilet` (`toilet_count`),
  KEY `ix_shown` (`shown`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `structure_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `structure_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dt` date,
  `property_id` int(11) NOT NULL DEFAULT -1,
  `structure_id` int(11) NOT NULL,
  `popularity` int(11) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_structure_property_dt` (`structure_id`, `property_id`, `dt`),
  CONSTRAINT `structure_statistic_ibfk_2` FOREIGN KEY (`structure_id`) REFERENCES `structure` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `visitor`
--

DROP TABLE IF EXISTS `visitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visitor` (
  `openid` varchar(64),
  `ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `phone` char(11) DEFAULT NULL,
  `family_structure` int(11) DEFAULT NULL,
  `income_lower` int(11) DEFAULT NULL,
  `income_upper` int(11) DEFAULT NULL,
  `occupation` varchar(50) DEFAULT NULL,
  `education` varchar(50) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `purchase_times` int(11) DEFAULT NULL,
  PRIMARY KEY (`openid`),
  KEY `ix_ts` (`ts`),
  KEY `ix_phone` (`phone`),
  CONSTRAINT `visitor_ibfk_1` FOREIGN KEY (`openid`) REFERENCES `weixin_profile` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `visitor_record`
--

DROP TABLE IF EXISTS `visitor_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visitor_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `openid` varchar(64) DEFAULT NULL,
  `phone` char(11) DEFAULT NULL,
  `family_structure` int(11) DEFAULT NULL,
  `income_lower` int(11) DEFAULT NULL,
  `income_upper` int(11) DEFAULT NULL,
  `occupation` varchar(50) DEFAULT NULL,
  `education` varchar(50) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `purchase_times` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_ts` (`ts`),
  KEY `ix_phone` (`phone`),
  CONSTRAINT `visitor_record_ibfk_1` FOREIGN KEY (`openid`) REFERENCES `weixin_profile` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `weixin_profile`
--

DROP TABLE IF EXISTS `weixin_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weixin_profile` (
  `openid` varchar(128) NOT NULL,
  `unionid` varchar(128) NOT NULL,
  `nickname` varchar(128) DEFAULT NULL,
  `sex` tinyint DEFAULT NULL,
  `headimgurl` varchar(512) DEFAULT NULL,
  `country` varchar(128) DEFAULT NULL,
  `province` varchar(128) DEFAULT NULL,
  `city` varchar(128) DEFAULT NULL,
  `lang` varchar(16) DEFAULT NULL,
  `last_login` datetime  ON UPDATE CURRENT_TIMESTAMP,
  `first_login` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`openid`),
  KEY (`unionid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-02 14:43:35
