CREATE DATABASE IF NOT EXISTS `cms` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `cms`;

CREATE TABLE IF NOT EXISTS `course` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL COMMENT '课程编号',
  `name` varchar(255) NOT NULL COMMENT '课程名称',
  `url` varchar(255) DEFAULT NULL COMMENT '课程链接',
  `price` int(11) NOT NULL COMMENT '课程价格',
  `category` varchar(255) DEFAULT NULL COMMENT '课程类别',
  `create_time` datetime DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  `modifier` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `course_code_uindex` (`code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `salt` varchar(50) NOT NULL,
  `create_time` datetime DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  `modifier` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

INSERT INTO `user` (`username`, `password`, `age`, `salt`, `create_time`, `creator`, `modify_time`, `modifier`)
SELECT 'admin', 'ef59aa69919a238746d4422a17f162b3b3002eaab2798e15baac3bb74e17cda5', NULL, 'cms_admin_salt_2026', NOW(), 'system', NOW(), 'system'
WHERE NOT EXISTS (SELECT 1 FROM `user` WHERE `username` = 'admin');

INSERT INTO `course` (`code`, `name`, `url`, `price`, `category`, `create_time`, `creator`, `modify_time`, `modifier`)
SELECT 'NOTICE', 'CHATGPT工具网站', 'https://openai.com', 0, '公告', NOW(), 'system', NOW(), 'system'
WHERE NOT EXISTS (SELECT 1 FROM `course` WHERE `code` = 'NOTICE');

INSERT INTO `course` (`code`, `name`, `url`, `price`, `category`, `create_time`, `creator`, `modify_time`, `modifier`)
SELECT 'DOCS', '收集整理的一些书籍和软件，免费分享给大家，点击课程链接即可获取', 'https://example.com/docs', 0, '资料', NOW(), 'system', NOW(), 'system'
WHERE NOT EXISTS (SELECT 1 FROM `course` WHERE `code` = 'DOCS');

INSERT INTO `course` (`code`, `name`, `url`, `price`, `category`, `create_time`, `creator`, `modify_time`, `modifier`)
SELECT 'AD-01', '5G时代必备 音视频WebRTC实时互动直播技术入门与实战', 'https://example.com/ad-01', 8, 'Android', NOW(), 'system', NOW(), 'system'
WHERE NOT EXISTS (SELECT 1 FROM `course` WHERE `code` = 'AD-01');

INSERT INTO `course` (`code`, `name`, `url`, `price`, `category`, `create_time`, `creator`, `modify_time`, `modifier`)
SELECT 'AD-02', 'Android 工程师（金职位）', 'https://example.com/ad-02', 30, 'Android', NOW(), 'system', NOW(), 'system'
WHERE NOT EXISTS (SELECT 1 FROM `course` WHERE `code` = 'AD-02');

INSERT INTO `course` (`code`, `name`, `url`, `price`, `category`, `create_time`, `creator`, `modify_time`, `modifier`)
SELECT 'AD-03', 'Android架构师之路 网络层架构设计与实战', 'https://example.com/ad-03', 5, 'Android', NOW(), 'system', NOW(), 'system'
WHERE NOT EXISTS (SELECT 1 FROM `course` WHERE `code` = 'AD-03');
