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

year = 2017
season = 1

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "DROP TABLE IF EXISTS `stocks_growth`;"
cursor.execute(sql)

sql = "CREATE TABLE `stocks_growth` (\
   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
   `code` varchar(10) NOT NULL DEFAULT '',\
   `mbrg` double NOT NULL DEFAULT '0' COMMENT '主营业务收入增长率(%)',\
   `nprg` double NOT NULL DEFAULT '0' COMMENT '净利润增长率(%)',\
   `nav` double NOT NULL DEFAULT '0' COMMENT '净资产增长率',\
   `targ` double NOT NULL DEFAULT '0' COMMENT '总资产增长率',\
   `epsg` double NOT NULL DEFAULT '0' COMMENT '每股收益增长率',\
   `seg` double NOT NULL DEFAULT '0' COMMENT '股东权益增长率',\
   PRIMARY KEY (`id`),\
   UNIQUE KEY `code` (`code`)\
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='成长能力';"
cursor.execute(sql)

try:
    df = ts.get_growth_data(year, season)
    if df is not None:
        for id in df.index:
            temp = df.ix[id]
            
            code = temp['code']
            
            # 以下先判断temp['']是否为NAN
            if temp['mbrg'] != temp['mbrg']:
                mbrg = 0.00
            else:
                mbrg = temp['mbrg']
            if temp['nprg'] != temp['nprg']:
                nprg = 0.00
            else:
                nprg = temp['nprg']
            if temp['nav'] != temp['nav']:
                nav = 0.00
            else:
                nav  = temp['nav']
            if temp['targ'] != temp['targ']:
                targ = 0.00
            else:
                targ = temp['targ']
            if temp['epsg'] != temp['epsg']:
                epsg = 0.00
            else:
                epsg = temp['epsg']
            if temp['seg'] != temp['seg']:
                seg = 0.00
            else:
                seg  = temp['seg']
                
            # 先查询是否已存在相同记录
            sql = "select code from stocks_growth where code='" + code + "'"
            cursor.execute(sql)
            sg_res = cursor.fetchone()
            if sg_res:
                continue
             
            sql = "insert into stocks_growth(code,mbrg,nprg,nav,targ,epsg,seg) values(%s,%s,%s,%s,%s,%s,%s)"
            param = (code, mbrg, nprg, nav, targ, epsg, seg)
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