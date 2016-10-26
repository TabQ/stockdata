# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import traceback
import os

print datetime.datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate >= '2016-09-01' and calendarDate <= '2016-09-03' order by calendarDate"
cursor.execute(sql)
dateRes = cursor.fetchall()

for dateRow in dateRes:
    date = dateRow[0]
    
    sql = "select code from stocks_info"
    cursor.execute(sql)
    codeRes = cursor.fetchall()
    
    for codeRow in codeRes:
        code = codeRow[0]
        
        try:
            df = ts.get_h_data(code=code, start=date, end=date)
            if df is not None:
                if date in df.index:
                    temp = df.ix[date]
                    
                    _open   = temp['open']
                    high    = temp['high']
                    close   = temp['close']
                    low     = temp['low']
                    volume  = temp['volume']
                    amount  = temp['amount']
                    
                    sql = "insert into h_data(code,date,open,high,close,low,volume,amount) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    param = (code, date, _open, high, close, low, volume, amount)
                    cursor.execute(sql, param)
                    conn.commit()
        except:
            f=open("errors/"+date+".log",'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            
cursor.close()
conn.close()

print datetime.datetime.now()