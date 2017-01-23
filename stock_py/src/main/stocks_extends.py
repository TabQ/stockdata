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

sql = "select code from stocks_info"

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    code = row[0]

    sql = "select close from k_data where code='"+code+"' order by date desc limit 1"
    cursor.execute(sql)
    res_today =  cursor.fetchone()
    if res_today:
        close_today = res_today[0]
    else:
        continue
    
    sql = "select close from k_data where code='"+code+"' order by date desc limit 1,1"
    cursor.execute(sql)
    res_yesterday = cursor.fetchone()
    if res_yesterday:
        close_yesterday = res_yesterday[0]
    else:
        continue

    p_change = (close_today - close_yesterday) * 100.00 / close_yesterday
    
    sql = "select code from stocks_extends where code='"+code+"'"
    cursor.execute(sql)
    res_exist = cursor.fetchone()
    
    if res_exist:
        sql = "update stocks_extends set p_change=%s where code=%s"
    else:
        sql = "insert into stocks_extends(p_change, code) values(%s, %s)"
        
    param = (p_change, code)
    cursor.execute(sql, param)
    conn.commit()
        
# stocks_extends入库结束记入日志
now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (4, now)
cursor.execute(sql, param)
conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()