import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

print datetime.datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (1, now)
cursor.execute(sql, param)
conn.commit()
 
sql = "drop table if exists stocks_info"
cursor.execute(sql)

sql = "CREATE TABLE `stocks_info` (\
  `id` int(10) unsigned NOT NULL auto_increment,\
  `code` varchar(10) NOT NULL DEFAULT '',\
  `name` char(30) NOT NULL DEFAULT '',\
  `industry` char(30) NOT NULL DEFAULT '',\
  `area` char(30) NOT NULL DEFAULT '',\
  `pe` double NOT NULL DEFAULT 0,\
  `outstanding` double NOT NULL DEFAULT 0,\
  `totals` double NOT NULL DEFAULT 0,\
  `totalAssets` double NOT NULL DEFAULT 0,\
  `liquidAssets` double NOT NULL DEFAULT 0,\
  `fixedAssets` double NOT NULL DEFAULT 0,\
  `reserved` double NOT NULL DEFAULT 0,\
  `reservedPerShare` double NOT NULL DEFAULT 0,\
  `esp` double NOT NULL DEFAULT 0,\
  `bvps` double NOT NULL DEFAULT 0,\
  `pb` double NOT NULL DEFAULT 0,\
  `timeToMarket` char(10) NOT NULL DEFAULT '',\
  `maxVol` double NOT NULL DEFAULT '0',\
  `maxVolDate` char(10) NOT NULL DEFAULT '',\
  `minPrice` double NOT NULL DEFAULT '0',\
  `minPriceDate` char(10) NOT NULL DEFAULT '',\
  PRIMARY KEY (`id`),\
  UNIQUE KEY `code` (`code`)\
) ENGINE=MyISAM DEFAULT CHARSET=utf8;"
cursor.execute(sql)

df = ts.get_stock_basics()
if df is not None:
    for code in df.index:
        temp = df.ix[code]
        sql = "insert into stocks_info(code,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        param = (code,temp['name'],temp['industry'],temp['area'],temp['pe'],temp['outstanding'],temp['totals'],temp['totalAssets'],temp['liquidAssets'],temp['fixedAssets'],temp['reserved'],temp['reservedPerShare'],temp['esp'],temp['bvps'],temp['pb'],temp['timeToMarket'])
        try:
            cursor.execute(sql, param)
            conn.commit()
        except Exception,e:
            print Exception,":",e

now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (2, now)
cursor.execute(sql, param)
conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()