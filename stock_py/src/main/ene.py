# -*- coding: utf-8 -*-

# ENE公式：N:=10(默认为11，取10方便计算);M1:=10;M2:=9;
# UPPER:(1+M1/100)*MA(CLOSE,N);
# LOWER:(1-M2/100)*MA(CLOSE,N);
# ENE:(UPPER+LOWER)/2;

import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

N = 10.00      # 默认为11，取10方便计算均线
M1 = 10.00
M2 = 9.00

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

today = str(date.today())

# today = '2016-10-24'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    # ene入库开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (16, now)
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "select p.code, high, close, low, ma10, timeToMarket from perday_info as p, stocks_info as s where p.code = s.code and date='" + today + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        high = row[1]
        close = row[2]
        low = row[3]
        ma10 = row[4]
        timeToMarket = row[5]
        
        if diff_between_two_days(today, timeToMarket) < 3*30:
            continue
        
        upper = (1 + M1/100) * ma10
        lower = (1 - M2/100) * ma10
        ene = (upper + lower) /2
        
        if high >= upper:
            sql = "select id from focus_pool where code='" + code + "' and typeId=13 and subTypeId=1"
            cursor.execute(sql)
            upper_res = cursor.fetchone()
            if upper_res:
                sql = "update focus_pool set count=count+1, latest=%s where id=%s"
                param = (today, upper_res[0])
            else:
                sql = "insert into focus_pool(code, date, typeId, subTypeId, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 13, 1, close)
                
            cursor.execute(sql, param)
            conn.commit()
            
        if low <= lower:
            sql = "select id from focus_pool where code='" + code + "' and typeId=14 and subTypeId=1"
            cursor.execute(sql)
            lower_res = cursor.fetchone()
            if lower_res:
                sql = "update focus_pool set count=count+1, latest=%s where id=%s"
                param = (today, lower_res[0])
            else:
                sql = "insert into focus_pool(code, date, typeId, subTypeId, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 14, 1, close)
                
            cursor.execute(sql, param)
            conn.commit()
    
    # ene入库结束־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (17, now)
    cursor.execute(sql, param)
    conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()