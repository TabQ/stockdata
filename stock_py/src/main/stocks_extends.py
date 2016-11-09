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

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

# stocks_extends入库开始记入日志
now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (3, now)
cursor.execute(sql, param)
conn.commit()

sql = "drop table if exists stocks_extends"
cursor.execute(sql)

sql = "CREATE TABLE `stocks_extends` (\
   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
   `code` varchar(10) NOT NULL DEFAULT '',\
   `maxVol` double NOT NULL DEFAULT '0',\
   `maxVolDate` char(10) NOT NULL DEFAULT '',\
   `minPrice` double NOT NULL DEFAULT '0',\
   `minPriceDate` char(10) NOT NULL DEFAULT '',\
   PRIMARY KEY (`id`),\
   UNIQUE KEY `code` (`code`)\
) ENGINE=MyISAM DEFAULT CHARSET=utf8;"
cursor.execute(sql)

sql = "select code from stocks_info"

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    code = row[0]

    # get max volume and min price
    try:
        df = ts.get_hist_data(code)
        if df is None:
            continue
    
        max_vol = 0
        maxvol_date = ''
        min_price = 1000
        min_date = ''
        for date in df.index:
            if df.ix[date]['volume'] > max_vol:
                max_vol = df.ix[date]['volume']
                maxvol_date = date
            if df.ix[date]['low'] < min_price:
                min_price = df.ix[date]['low']
                min_date = date
                
        sql = "insert into stocks_extends(code,maxVol,maxVolDate,minPrice,minPriceDate) values(%s,%s,%s,%s,%s)"
        param = (code, max_vol, maxvol_date, min_price, min_date)
        cursor.execute(sql, param)
        conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
    
# stocks_extends入库结束记入日志
now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (4, now)
cursor.execute(sql, param)
conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()