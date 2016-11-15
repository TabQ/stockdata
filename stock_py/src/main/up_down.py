# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

def diff_between_two_days(day1, day2):
    if day1 == '0' or day2 == '0':
        return 0
    
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

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    # 每日涨跌幅入库开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (18, now)
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "select k.code, close, timeToMarket from k_data as k, stocks_info as s where k.code = s.code and date='" + today + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        close = row[1]
        timetomarket = row[2]
        
        if diff_between_two_days(today, timetomarket) < 30:
            continue
        
        sql = "select close from k_data where code = %s and date < %s order by date desc limit 1"
        param = (code, today)
        cursor.execute(sql, param)
        yest_res = cursor.fetchone()
        
        if yest_res:
            yest_close = yest_res[0]
            percent = (close - yest_close) * 100.00 / yest_close
            if abs(percent) > 2.00:
                sql = "insert into up_down(code, date, percent) values(%s, %s, %s)"
                param = (code, today, percent)
                cursor.execute(sql, param)
                conn.commit()
                
    # 每日涨跌幅入库结束
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (19, now)
    cursor.execute(sql, param)
    conn.commit()
    
cursor.close()
conn.close()

print datetime.datetime.now()