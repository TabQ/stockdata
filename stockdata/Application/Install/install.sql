DROP TABLE IF EXISTS `focus_pool`;
CREATE TABLE `focus_pool` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` char(10) NOT NULL DEFAULT '',
  `count` smallint(3) unsigned NOT NULL DEFAULT '1',
  `latest` char(10) NOT NULL DEFAULT '',
  `man_date` char(10) NOT NULL DEFAULT '',
  `typeId` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `subTypeId` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '子类型：1.自动；2.手动',
  `cost_price` double NOT NULL DEFAULT '0.00' COMMENT '成本价',
  `yield_rate` double NOT NULL DEFAULT '0.00' COMMENT '收益率',
  PRIMARY KEY (`id`),
  KEY `yield_rate` (`yield_rate`),
  UNIQUE KEY `code_type_subtype` (`code`, `typeId`, `subTypeId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `focus_type`;
CREATE TABLE `focus_type` (
  `id` SMALLINT(5) unsigned NOT NULL DEFAULT 0,
  `name` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='关注类型';
INSERT INTO `focus_type` VALUES(1, '成交量突破');
INSERT INTO `focus_type` VALUES(2, '上升波段');
INSERT INTO `focus_type` VALUES(3, '横盘整理');
INSERT INTO `focus_type` VALUES(4, '看涨');
INSERT INTO `focus_type` VALUES(5, '看跌');
INSERT INTO `focus_type` VALUES(6, '出贷');
INSERT INTO `focus_type` VALUES(7, '下降波段');
INSERT INTO `focus_type` VALUES(8, '成交量突破回踩开始');
INSERT INTO `focus_type` VALUES(9, '成交量突破回踩结束');
INSERT INTO `focus_type` VALUES(10, '密切关注，随时建仓');

DROP TABLE IF EXISTS `action_type`;
CREATE TABLE `action_type` (
  `id` SMALLINT(5) unsigned NOT NULL DEFAULT 0,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='动作类型';

DROP TABLE IF EXISTS `action_log`;
CREATE TABLE `action_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `action_id` SMALLINT(5) unsigned NOT NULL DEFAULT 0,
  `time`	int(11) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='动作日志';

DROP TABLE IF EXISTS `stocks_info`;
CREATE TABLE `stocks_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `name` char(30) NOT NULL DEFAULT '',
  `industry` char(30) NOT NULL DEFAULT '',
  `area` char(30) NOT NULL DEFAULT '',
  `pe` double NOT NULL DEFAULT '0',
  `outstanding` double NOT NULL DEFAULT '0',
  `totals` double NOT NULL DEFAULT '0',
  `totalAssets` double NOT NULL DEFAULT '0',
  `liquidAssets` double NOT NULL DEFAULT '0',
  `fixedAssets` double NOT NULL DEFAULT '0',
  `reserved` double NOT NULL DEFAULT '0',
  `reservedPerShare` double NOT NULL DEFAULT '0',
  `esp` double NOT NULL DEFAULT '0',
  `bvps` double NOT NULL DEFAULT '0',
  `pb` double NOT NULL DEFAULT '0',
  `timeToMarket` char(10) NOT NULL DEFAULT '',
  `maxVol` double NOT NULL DEFAULT '0',
  `maxVolDate` char(10) NOT NULL DEFAULT '',
  `minPrice` double NOT NULL DEFAULT '0',
  `minPriceDate` char(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `hist_info`;
CREATE TABLE `hist_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` char(10) NOT NULL DEFAULT '',
  `open` double NOT NULL DEFAULT '0',
  `high` double NOT NULL DEFAULT '0',
  `close` double NOT NULL DEFAULT '0',
  `low` double NOT NULL DEFAULT '0',
  `volume` double NOT NULL DEFAULT '0',
  `price_change` double NOT NULL DEFAULT '0',
  `p_change` double NOT NULL DEFAULT '0',
  `ma5` double NOT NULL DEFAULT '0',
  `ma10` double NOT NULL DEFAULT '0',
  `ma20` double NOT NULL DEFAULT '0',
  `v_ma5` double NOT NULL DEFAULT '0',
  `v_ma10` double NOT NULL DEFAULT '0',
  `v_ma20` double NOT NULL DEFAULT '0',
  `turnover` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY code_date (`code`, `date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `perday_info`;
CREATE TABLE `perday_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` char(10) NOT NULL DEFAULT '',
  `open` double NOT NULL DEFAULT '0',
  `high` double NOT NULL DEFAULT '0',
  `close` double NOT NULL DEFAULT '0',
  `low` double NOT NULL DEFAULT '0',
  `volume` double NOT NULL DEFAULT '0',
  `price_change` double NOT NULL DEFAULT '0',
  `p_change` double NOT NULL DEFAULT '0',
  `ma5` double NOT NULL DEFAULT '0',
  `ma10` double NOT NULL DEFAULT '0',
  `ma20` double NOT NULL DEFAULT '0',
  `v_ma5` double NOT NULL DEFAULT '0',
  `v_ma10` double NOT NULL DEFAULT '0',
  `v_ma20` double NOT NULL DEFAULT '0',
  `turnover` double NOT NULL DEFAULT '0',
  `p2ma20` double NOT NULL DEFAULT '0',
  `p2min` double NOT NULL DEFAULT '0',
  `ma20_2_min` double NOT NULL DEFAULT '0',
  `v2ma20` double NOT NULL DEFAULT '0',
  `v2max` double NOT NULL DEFAULT '0',
  `vma20_2_max` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY code_date (`code`, `date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `trade_cal`;
CREATE TABLE `trade_cal` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `exchangeCD` char(10) NOT NULL DEFAULT '',
  `calendarDate` char(10) NOT NULL DEFAULT '',
  `isOpen` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `prevTradeDate` char(10) NOT NULL DEFAULT '',
  `isWeekEnd` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `isMonthEnd` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `isQuarterEnd` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `isYearEnd` tinyint(1) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `calendarDate` (`calendarDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='交易所交易日历';

