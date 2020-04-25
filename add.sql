/*
 Navicat Premium Data Transfer

 Source Server         : yezi
 Source Server Type    : MySQL
 Source Server Version : 50718
 Source Host           : localhost:3306
 Source Schema         : zerd

 Target Server Type    : MySQL
 Target Server Version : 50718
 File Encoding         : 65001

 Date: 09/04/2019 13:24:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for banner
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `nickname` varchar(250) DEFAULT NULL COMMENT '用户名称，通常作为标识',
	  `headpic` varchar(500) DEFAULT NULL COMMENT '用户头像',
	  `openid` varchar(250) DEFAULT NULL COMMENT '用户ID',
	  `unionid` varchar(250) DEFAULT NULL COMMENT '用户ID',
	  `mobile` varchar(255) DEFAULT NULL COMMENT '用户手机',
	  `shop_id` varchar(255) DEFAULT NULL COMMENT '用户手机',
	  `is_checked` int(1) DEFAULT NULL,
	  `is_in_contract` int(1) DEFAULT NULL,
	  `update_time` int(11) DEFAULT NULL,
	  `create_time` int(11) DEFAULT NULL,
	  `delete_time` int(11) DEFAULT NULL,
	  `is_shop_owner` smallint(6) DEFAULT NULL,
	  `extend` varchar(500) DEFAULT NULL COMMENT '用户头像',
	  `auth` smallint(6) DEFAULT NULL COMMENT '用户头像',
	  `status` smallint(6) DEFAULT NULL COMMENT '用户头像',
	  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='用户管理表';

