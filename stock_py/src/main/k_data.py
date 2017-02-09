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

sql = "drop table if exists k_data"
cursor.execute(sql)

sql = "CREATE TABLE `k_data` (\
   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,\
   `code` varchar(10) NOT NULL DEFAULT '',\
   `date` char(10) NOT NULL DEFAULT '',\
   `type` char(1) NOT NULL DEFAULT 'S',\
   `open` double NOT NULL DEFAULT '0',\
   `high` double NOT NULL DEFAULT '0',\
   `low` double NOT NULL DEFAULT '0',\
   `close` double NOT NULL DEFAULT '0',\
   `volume` double NOT NULL DEFAULT '0',\
   PRIMARY KEY (`id`),\
   UNIQUE KEY `code_date_type` (`code`,`date`,`type`)\
) ENGINE=MyISAM DEFAULT CHARSET=utf8;"
cursor.execute(sql)

sql = "select code, type from stocks_info"

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    code = row[0]
    type = row[1]
    
    try:
        if type == 'I':
            df = ts.get_k_data(code, index=True)
        else:
            df = ts.get_k_data(code)
        if df is not None:
            for id in df.index:
                temp = df.ix[id]
                sql = "insert into k_data(code, date, open, high, low, close, volume, type) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (temp['code'],temp['date'],temp['open'],temp['high'],temp['low'],temp['close'],temp['volume'],type)
                cursor.execute(sql, param)
                conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()            
            
cursor.close()
conn.close()

print datetime.datetime.now()