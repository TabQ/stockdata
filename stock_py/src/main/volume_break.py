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

# today = '2016-11-11'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    
    sql = "select k.code,volume,close,timeToMarket from k_data as k, stocks_info as s where k.code = s.code and date='" + today + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        volume = row[1]
        close = row[2]
        timeToMarket = row[3]
        
        if diff_between_two_days(today, timeToMarket) < 3*30:
            continue
        
        vma5 = vma20 = 0
        vma_sql = "select volume from k_data where code=%s and date < %s order by date desc limit 20"
        vma_param = (code, today)
        cursor.execute(vma_sql, vma_param)
        vma_res = cursor.fetchall()
        day = 0
        for vma_row in vma_res:
            if day >= 5:
                vma20 += vma_row[0]
            else:
                vma5 += vma_row[0]
                vma20 += vma_row[0]
                
            day += 1
            
        vma5 /= 5
        vma20 /= 20
        v2ma5 = volume / vma5
        v2ma20 = volume / vma20
        
        if v2ma5 >= 2.0:
            sql = "select id from focus_pool where code='" + code + "' and type_id=2 and subtype_id=1"
            cursor.execute(sql)
            fp_res = cursor.fetchone()
            if fp_res:
                sql = "update focus_pool set count=count+1, latest=%s where id=%s"
                param = (today, fp_res[0])
                cursor.execute(sql, param)
                conn.commit()
            else:
                sql = "insert into focus_pool(code,date,type_id,subtype_id,cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 2, 1, close)
                cursor.execute(sql, param)
                conn.commit()
                
                sql = "insert into volume_break(code,date,v2ma5,v2ma20) values(%s,%s,%s,%s)"
                param = (code, today, v2ma5, v2ma20)
                cursor.execute(sql, param)
                conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()