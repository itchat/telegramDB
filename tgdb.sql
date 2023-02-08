/*
 Navicat Premium Data Transfer

 Source Server         : 155.248.178.177
 Source Server Type    : MySQL
 Source Server Version : 50741 (5.7.41)
 Source Host           : 155.248.178.177:3306
 Source Schema         : tgdb

 Target Server Type    : MySQL
 Target Server Version : 50741 (5.7.41)
 File Encoding         : 65001

 Date: 08/02/2023 08:43:42
*/

CREATE DATABASE tgdb;
USE tgdb;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `id` int(11) NOT NULL,
  `text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
