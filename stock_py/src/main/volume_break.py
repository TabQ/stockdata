# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

def diff_between_tow_days(day1, day2):
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

today = str(date.today())

today = '2016-02-15'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    # perday_info入库开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (11, now)
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "select p.code, open, high, close, low, timeToMarket from perday_info as p, stocks_info as s where p.code = s.code and v2ma20 > 2.90 and date='" + today + "' order by v2ma20 desc, vma20_2_max"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        _open = row[1]
        high = row[2]
        close = row[3]
        low = row[4]
        timeToMarket = row[5]
        
        if (_open == high and _open == close and _open == low) or diff_between_tow_days(today, timeToMarket) < 3*30:
            continue
        
        sql = "select other_date from focus_pool where code='" + code + "'"
        cursor.execute(sql)
        fp_res = cursor.fetchone()
        if fp_res:
            other_date = fp_res[0] + "," + today
            sql = "update focus_pool set count=count+1, other_date=%s where code=%s"
            param = (other_date, code)
        else:
            sql = "insert into focus_pool(code, date, typeId, subTypeId, cost_price) values(%s,%s,%s,%s,%s)"
            param = (code, today, 1, 1, close)
            
        cursor.execute(sql, param)
        conn.commit()
        
    # perday_info入库开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (12, now)
    cursor.execute(sql, param)
    conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()