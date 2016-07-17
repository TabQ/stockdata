# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

print datetime.datetime.now()

today = str(date.today())

today = '2016-02-16'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate ='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    
    # focus_pool_rate开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (14, now)
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "select code, cost_price, id from focus_pool where date < '" + today + "'"
    cursor.execute(sql)
    fpRes = cursor.fetchall()
    
    for fpRow in fpRes:
        sql = "select close from perday_info where code=%s and date=%s"
        param = (fpRow[0], today)
        cursor.execute(sql, param)
        pi = cursor.fetchone()
        
        if pi:
            yield_rate = (pi[0] - fpRow[1]) * 100 / fpRow[1]
            sql = "update focus_pool set yield_rate=%s where id=%s"
            param = (yield_rate, fpRow[2])
            cursor.execute(sql, param)
            conn.commit()
            
    # focus_pool_rate结束־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (15, now)
    cursor.execute(sql, param)
    conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()