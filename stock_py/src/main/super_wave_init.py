# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

def diff_between_two_days(day1, day2):
    if day1 == '0' or day2 == '0':
        return 0;
    
    second1 = datetime.datetime.strptime(day1, "%Y-%m-%d")
    second1 = time.mktime(second1.timetuple())
    
    second2 = datetime.datetime.strptime(day2, "%Y%m%d")
    second2 = time.mktime(second2.timetuple())
    
    if(second1 < second2):
        tmp = second2
        second2 = second1
        second1 = tmp
        
    return (second1 - second2) / 86400

print datetime.datetime.now()

today = '2016-06-30'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    sql = "select p.code, close, timeToMarket from perday_info as p, stocks_info as s where p.code=s.code and date='"+today+"'"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        close = row[1]
        timeToMarket = row[2]
        
        if diff_between_two_days(today, timeToMarket) < 3*30:
            continue
        
        sql = "insert into super_wave(code,date,min,max) values(%s,%s,%s,%s)"
        param = (code, today, close, close)
        cursor.execute(sql, param)
        conn.commit()
        
cursor.close()
conn.close()

print datetime.datetime.now()