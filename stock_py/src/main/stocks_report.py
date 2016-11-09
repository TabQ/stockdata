# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import traceback
import sys

print datetime.datetime.now()

today = str(date.today())

year = 2016
season = 3

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "DROP TABLE IF EXISTS `stocks_report`;"
cursor.execute(sql)

sql = "CREATE TABLE `stocks_report` (\
   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
   `code` varchar(10) NOT NULL DEFAULT '',\
   `eps` double NOT NULL DEFAULT '0' COMMENT '每股收益',\
   `eps_yoy` double NOT NULL DEFAULT '0' COMMENT '每股收益同比(%)',\
   `bvps` double NOT NULL DEFAULT '0' COMMENT '每股净资产',\
   `roe` double NOT NULL DEFAULT '0' COMMENT '净资产收益率(%)',\
   `epcf` double NOT NULL DEFAULT '0' COMMENT '每股现金流量(元)',\
   `net_profits` double NOT NULL DEFAULT '0' COMMENT '净利润(万元)',\
   `profits_yoy` double NOT NULL DEFAULT '0' COMMENT '净利润同比(%)',\
   `distrib` char(30) NOT NULL DEFAULT '' COMMENT '分配方案',\
   `report_date` char(10) NOT NULL DEFAULT '' COMMENT '发布日期',\
   PRIMARY KEY (`id`),\
   UNIQUE KEY `code` (`code`)\
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='业绩报告（主表）';"
cursor.execute(sql)

try:
    df = ts.get_report_data(year, season)
    if df is not None:
        for id in df.index:
            temp = df.ix[id]
            
            code = temp['code']
            
            # 以下先判断temp['']是否为NAN
            if temp['eps'] != temp['eps']:
                eps = 0.00
            else:
                eps = temp['eps']
            if temp['eps_yoy'] != temp['eps_yoy']:
                eps_yoy = 0.00
            else:
                eps_yoy = temp['eps_yoy']
            if temp['bvps'] != temp['bvps']:
                bvps = 0.00
            else:
                bvps = temp['bvps']
            if temp['roe'] != temp['roe']:
                roe = 0.00
            else:
                roe = temp['roe']
            if temp['epcf'] != temp['epcf']:
                epcf = 0.00
            else:
                epcf = temp['epcf']
            if temp['net_profits'] != temp['net_profits']:
                net_profits = 0.00
            else:
                net_profits = temp['net_profits']
            if temp['profits_yoy'] != temp['profits_yoy']:
                profits_yoy = 0.00
            else:
                profits_yoy = temp['profits_yoy']
            if temp['distrib'] != temp['distrib']:
                distrib = ''
            else:
                distrib = temp['distrib']
            
            report_date = temp['report_date']
            
            # 先查询是否已存在相同记录
            sql = "select code from stocks_report where code='" + code + "'"
            cursor.execute(sql)
            sr_res = cursor.fetchone()
            if sr_res:
                continue
            
            sql = "insert into stocks_report(code,eps,eps_yoy,bvps,roe,epcf,net_profits,profits_yoy,distrib,report_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            param = (code, eps, eps_yoy, bvps, roe, epcf, net_profits, profits_yoy, distrib, report_date)
            try:
                cursor.execute(sql, param)
                conn.commit()
            except Exception,e:
                print Exception,":",e
except:
    f=open("errors/"+today+".log",'a')
    traceback.print_exc(file=f)
    f.flush()
    f.close()
    
cursor.close()
conn.close()

print datetime.datetime.now()