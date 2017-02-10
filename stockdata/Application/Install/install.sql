DROP TABLE IF EXISTS `focus_pool`;
CREATE TABLE `focus_pool` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` char(10) NOT NULL DEFAULT '',
  `man_date` char(10) NOT NULL DEFAULT '',
  `type_id` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `subtype_id` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '子类型：1.自动；2.手动',
  `cost_price` double NOT NULL DEFAULT '0.00' COMMENT '成本价',
  `yield_rate` double NOT NULL DEFAULT '0.00' COMMENT '收益率',
  `rec3minus` double NOT NULL DEFAULT '0.00' COMMENT '最近3天收益率上升最快',
  `rec5minus` double NOT NULL DEFAULT '0.00' COMMENT '最近5天收益率上升最快',
  `rec3tops` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '最近3天收益率排top10数目',
  `rec5tops` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '最近5天收益率排top10数目',
  `rec3topsdate` char(10) NOT NULL DEFAULT '' COMMENT '记录最近3天收益率排top10数目的日期',
  `rec5topsdate` char(10) NOT NULL DEFAULT '' COMMENT '记录最近5天收益率排top10数目的日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_date_type_subtype` (`code`, `date`, `type_id`, `subtype_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `focus_type`;
CREATE TABLE `focus_type` (
  `id` SMALLINT(5) unsigned NOT NULL DEFAULT 0,
  `name` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='关注类型';
INSERT INTO `focus_type` VALUES(1, '近期关注');
INSERT INTO `focus_type` VALUES(2, 'ene打上轨');
INSERT INTO `focus_type` VALUES(3, 'ene打下轨');
INSERT INTO `focus_type` VALUES(4, 'ene接近下轨');
INSERT INTO `focus_type` VALUES(5, '成交量突破5d');
INSERT INTO `focus_type` VALUES(6, '成交量突破10d');
INSERT INTO `focus_type` VALUES(7, '成交量突破20d');
INSERT INTO `focus_type` VALUES(8, '缩量max');
INSERT INTO `focus_type` VALUES(9, '缩量max_5d');
INSERT INTO `focus_type` VALUES(10, '缩量max_10d');
INSERT INTO `focus_type` VALUES(11, '缩量max_20d');
INSERT INTO `focus_type` VALUES(12, '缩量max_60d');
INSERT INTO `focus_type` VALUES(13, '缩量max_120d');
INSERT INTO `focus_type` VALUES(14, '缩量ma_5d');
INSERT INTO `focus_type` VALUES(15, '缩量ma_10d');
INSERT INTO `focus_type` VALUES(16, '缩量ma_20d');
INSERT INTO `focus_type` VALUES(17, '缩量ma_60d');
INSERT INTO `focus_type` VALUES(18, '缩量ma_120d');
INSERT INTO `focus_type` VALUES(19, 'ene候选');
INSERT INTO `focus_type` VALUES(20, 'ene弃选');

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
  `type` char(1) NOT NULL DEFAULT 'S',
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_type` (`code`,`type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `stocks_info`(code, type, name) VALUES('000001', 'I', '上证指数');
INSERT INTO `stocks_info`(code, type, name) VALUES('399001', 'I', '深证成指');
INSERT INTO `stocks_info`(code, type, name) VALUES('399005', 'I', '中小板指');
INSERT INTO `stocks_info`(code, type, name) VALUES('399006', 'I', '创业板指');

DROP TABLE IF EXISTS `stocks_report`;
CREATE TABLE `stocks_report` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `eps` double NOT NULL DEFAULT '0' COMMENT '每股收益',
  `eps_yoy` double NOT NULL DEFAULT '0' COMMENT '每股收益同比(%)',
  `bvps` double NOT NULL DEFAULT '0' COMMENT '每股净资产',
  `roe` double NOT NULL DEFAULT '0' COMMENT '净资产收益率(%)',
  `epcf` double NOT NULL DEFAULT '0' COMMENT '每股现金流量(元)',
  `net_profits` double NOT NULL DEFAULT '0' COMMENT '净利润(万元)',
  `profits_yoy` double NOT NULL DEFAULT '0' COMMENT '净利润同比(%)',
  `distrib` char(30) NOT NULL DEFAULT '' COMMENT '分配方案',
  `report_date` char(10) NOT NULL DEFAULT '' COMMENT '发布日期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='业绩报告（主表）';

DROP TABLE IF EXISTS `stocks_growth`;
CREATE TABLE `stocks_growth` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `mbrg` double NOT NULL DEFAULT '0' COMMENT '主营业务收入增长率(%)',
  `nprg` double NOT NULL DEFAULT '0' COMMENT '净利润增长率(%)',
  `nav` double NOT NULL DEFAULT '0' COMMENT '净资产增长率',
  `targ` double NOT NULL DEFAULT '0' COMMENT '总资产增长率',
  `epsg` double NOT NULL DEFAULT '0' COMMENT '每股收益增长率',
  `seg` double NOT NULL DEFAULT '0' COMMENT '股东权益增长率',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='成长能力';

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

CREATE TABLE `k_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` char(10) NOT NULL DEFAULT '',
  `type` char(1) NOT NULL DEFAULT 'S',
  `open` double NOT NULL DEFAULT '0',
  `high` double NOT NULL DEFAULT '0',
  `low` double NOT NULL DEFAULT '0',
  `close` double NOT NULL DEFAULT '0',
  `volume` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_date_type` (`code`,`date`,`type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `super_wave`;
CREATE TABLE `super_wave` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `summit_date` char(10) NOT NULL DEFAULT '' COMMENT '当前波峰/波谷日期',
  `cost_date` char(10) NOT NULL DEFAULT '' COMMENT '开始计算成本日期',
  `man_date` char(10) NOT NULL DEFAULT '' COMMENT '标识日期',
  `min` double NOT NULL DEFAULT '0',
  `max` double NOT NULL DEFAULT '0',
  `cost_price` double NOT NULL DEFAULT '0.00' COMMENT '成本价',
  `yield_rate` double NOT NULL DEFAULT '0.00' COMMENT '收益率',
  `flag` tinyint(1) unsigned NOT NULL DEFAULT 0 COMMENT '标识',
  `percent` double NOT NULL DEFAULT '0' COMMENT '超涨/超跌的百分比',
  `cur_per` double NOT NULL DEFAULT '0' COMMENT '当前超涨/超跌的百分比',
  `direction` tinyint(1) NOT NULL DEFAULT '1' COMMENT '超涨超跌标识(1超涨/-1超跌)',
  PRIMARY KEY (`id`),
  UNIQUE KEY code (`code`),
  KEY dir_curper (`direction`, `cur_per`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='寻找超涨/超跌';

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

DROP TABLE IF EXISTS `top_list`;
CREATE TABLE `top_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `date` char(10) NOT NULL DEFAULT '',
  `code` varchar(10) NOT NULL DEFAULT '',
  `name` char(30) NOT NULL DEFAULT '',
  `pchange` double NOT NULL DEFAULT '0' COMMENT '当日涨跌幅',
  `amount` double NOT NULL DEFAULT '0' COMMENT '龙虎榜成交额(万)',
  `buy` double NOT NULL DEFAULT '0' COMMENT '买入额（万）',
  `sell` double NOT NULL DEFAULT '0' COMMENT '卖入额（万）',
  `bratio` char(10) NOT NULL DEFAULT '' COMMENT '买入占总成交比例',
  `sratio` char(10) NOT NULL DEFAULT '' COMMENT '卖出占总成交比例',
  `reason` varchar(255) NOT NULL DEFAULT '' COMMENT '上榜原因',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='每日龙虎榜列表';

DROP TABLE IF EXISTS `cap_tops`;
CREATE TABLE `cap_tops` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `name` char(30) NOT NULL DEFAULT '',
  `count` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '上榜次数',
  `bamount` double NOT NULL DEFAULT '0' COMMENT '累积购买额（万）',
  `samount` double NOT NULL DEFAULT '0' COMMENT '累积卖出额（万）',
  `net` double NOT NULL DEFAULT '0' COMMENT '净额（万）',
  `bcount` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '买入席位数',
  `scount` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '卖出席位数',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='个股上榜统计';

DROP TABLE IF EXISTS `broker_tops`;
CREATE TABLE `broker_tops` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `broker` varchar(255) NOT NULL DEFAULT '' COMMENT '营业部名称',
  `count` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '上榜次数',
  `bamount` double NOT NULL DEFAULT '0' COMMENT '累积购买额（万）',
  `samount` double NOT NULL DEFAULT '0' COMMENT '累积卖出额（万）',
  `bcount` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '买入席位数',
  `scount` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '卖出席位数',
  `top3` varchar(255) NOT NULL DEFAULT '' COMMENT '买入前三股票',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='营业部上榜统计';

DROP TABLE IF EXISTS `inst_tops`;
CREATE TABLE `inst_tops` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `name` char(30) NOT NULL DEFAULT '',
  `bamount` double NOT NULL DEFAULT '0' COMMENT '累积购买额（万）',
  `samount` double NOT NULL DEFAULT '0' COMMENT '累积卖出额（万）',
  `bcount` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '买入次数',
  `scount` smallint(3) unsigned NOT NULL DEFAULT '0' COMMENT '卖出次数',
  `net` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='机构席位追踪';

DROP TABLE IF EXISTS `inst_detail`;
CREATE TABLE `inst_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `name` char(30) NOT NULL DEFAULT '',
  `date` char(10) NOT NULL DEFAULT '',
  `bamount` double NOT NULL DEFAULT '0' COMMENT '机构席位买入额（万）',
  `samount` double NOT NULL DEFAULT '0' COMMENT '机构席位卖出额（万）',
  `type` varchar(255) NOT NULL DEFAULT '' COMMENT '类型',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='机构成交明细';

DROP TABLE IF EXISTS `stocks_concept`;
CREATE TABLE `stocks_concept` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `name` char(30) NOT NULL DEFAULT '',
  `concept` char(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='概念分类';

DROP TABLE IF EXISTS `stocks_extends`;
CREATE TABLE `stocks_extends` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` varchar(10) NOT NULL DEFAULT '',
  `type` char(1) NOT NULL DEFAULT 'S',
  `p_change` double NOT NULL DEFAULT '0' COMMENT '涨跌幅',
  `p2max` double NOT NULL DEFAULT '0' COMMENT '当前收盘价与历史最高收盘价之比',
  `dist_per` double NOT NULL DEFAULT '0' COMMENT '最低价到ene下轨的距离相当于轨道间距的百分比',
  `ma5` double NOT NULL DEFAULT '0',
  `ma10` double NOT NULL DEFAULT '0',
  `ma13` double NOT NULL DEFAULT '0' COMMENT '主要用来计算板块指数及个股持股线',
  `ma14` double NOT NULL DEFAULT '0' COMMENT '主要用来计算板块指数及个股持股线',
  `ma15` double NOT NULL DEFAULT '0' COMMENT '主要用来计算板块指数及个股持股线',
  `ma20` double NOT NULL DEFAULT '0',
  `ma60` double NOT NULL DEFAULT '0',
  `ma120` double NOT NULL DEFAULT '0',
  `ma250` double NOT NULL DEFAULT '0',
  `v_ma5` double NOT NULL DEFAULT '0',
  `v_ma10` double NOT NULL DEFAULT '0',
  `v_ma20` double NOT NULL DEFAULT '0',
  `v_ma60` double NOT NULL DEFAULT '0',
  `v_ma120` double NOT NULL DEFAULT '0',
  `max_vol5` double NOT NULL DEFAULT '0',
  `max_vol10` double NOT NULL DEFAULT '0',
  `max_vol20` double NOT NULL DEFAULT '0',
  `max_vol60` double NOT NULL DEFAULT '0',
  `max_vol120` double NOT NULL DEFAULT '0',
  `turnover` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY code_date_type (`code`, `date`, `type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `volume`;
CREATE TABLE `volume` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `date` varchar(10) NOT NULL DEFAULT '',
  `v2ma5d` double NOT NULL DEFAULT '0',
  `v2ma10d` double NOT NULL DEFAULT '0',
  `v2ma20d` double NOT NULL DEFAULT '0',
  `v2ma60d` double NOT NULL DEFAULT '0',
  `v2ma120d` double NOT NULL DEFAULT '0',
  `v2max` double NOT NULL DEFAULT '0',
  `v2max5d` double NOT NULL DEFAULT '0',
  `v2max10d` double NOT NULL DEFAULT '0',
  `v2max20d` double NOT NULL DEFAULT '0',
  `v2max60d` double NOT NULL DEFAULT '0',
  `v2max120d` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_date` (`code`, `date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `stocks_summit`;
CREATE TABLE `stocks_summit` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '',
  `type` char(1) NOT NULL DEFAULT 'S',
  `max_vol` double NOT NULL DEFAULT '0',
  `max_price` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY code_type (`code`, `type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `test_yield`;
CREATE TABLE `test_yield` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `start_date` char(10) NOT NULL DEFAULT '',
  `end_date` char(10) NOT NULL DEFAULT '',
  `sum_yield` double NOT NULL DEFAULT '0',
  `type` char(1) NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id`),
  UNIQUE KEY start_date_type (`start_date`, `type`),
  UNIQUE KEY end_date_type (`end_date`, `type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;