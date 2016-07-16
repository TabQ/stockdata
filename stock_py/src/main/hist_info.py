# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

print datetime.datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select code from stocks_info"
cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    code = row[0]
    
    df = ts.get_hist_data(code)
    if df is None:
        continue
    
    for date in df.index:
        temp = df.ix[date]
        sql = "insert into hist_info(code,date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        param = (code,date,temp['open'],temp['high'],temp['close'],temp['low'],temp['volume'],temp['price_change'],temp['p_change'],temp['ma5'],temp['ma10'],temp['ma20'],temp['v_ma5'],temp['v_ma10'],temp['v_ma20'],temp['turnover'])
        cursor.execute(sql, param)
        conn.commit()
        
cursor.close()
conn.close()

print datetime.datetime.now()