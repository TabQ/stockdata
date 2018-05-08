# -*- coding: utf-8 -*-
from __future__ import division
import tushare as ts
import MySQLdb
from datetime import date
import time

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

today = str(date.today())
morning_start = time.mktime(time.strptime(today + ' 09:25:00', '%Y-%m-%d %H:%M:%S'))
morning_end = time.mktime(time.strptime(today + ' 11:30:00', '%Y-%m-%d %H:%M:%S'))
afternoon_start = time.mktime(time.strptime(today + ' 13:00:00', '%Y-%m-%d %H:%M:%S'))
afternoon_end = time.mktime(time.strptime(today + ' 15:00:00', '%Y-%m-%d %H:%M:%S'))
while(True):
    now = time.time()
    nowstr = time.strftime('%H:%M:%S', time.localtime(now))
    if now < morning_start or (now > morning_end and now < afternoon_start):
        continue
    if now > afternoon_end:
        break

    try:
        df = ts.get_today_all()
        if df is not None:
            for index in df.index:
                temp = df.ix[index]
                if temp['changepercent'] > 2:
                    if temp['trade'] == temp['open'] and temp['open'] == temp['high'] and temp['high'] == temp['low']:
                        continue
                    
                    sql = "insert into `watchall`(`code`, `date`, `now`, `trade`, `changepercent`, `amt2nmc`) values(%s, %s, %s, %s, %s, %s)"
                    param = (temp['code'], today, nowstr, temp['trade'], temp['changepercent'], temp['amount']*0.0001/temp['nmc'])
                    cursor.execute(sql, param)
                    conn.commit()
    except:
        pass
                
cursor.close()
conn.close()