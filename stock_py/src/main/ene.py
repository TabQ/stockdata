# -*- coding: utf-8 -*-

# ENE公式：N:=10;M1:=11;M2:=9;
# UPPER:(1+M1/100)*MA(CLOSE,N);
# LOWER:(1-M2/100)*MA(CLOSE,N);
# ENE:(UPPER+LOWER)/2;

import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

N = 10.00
M1 = 11.00
M2 = 9.00

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
    # ene入库开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (16, now)
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "select k.code, high, close, low, timeToMarket from k_data as k, stocks_info as s where k.code = s.code and date='" + today + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    close_lower_list = []
    
    for row in results:
        code = row[0]
        high = row[1]
        close = row[2]
        low = row[3]
        timeToMarket = row[4]
        
        if diff_between_two_days(today, timeToMarket) < 3*30:
            continue
        
        # 计算ma10
        ma10 = 0
        ma_sql = "select close from k_data where code=%s and date <= %s order by date desc limit 10"
        ma_param = (code, today)
        cursor.execute(ma_sql, ma_param)
        ma_res = cursor.fetchall()
        for ma_row in ma_res:
            ma10 += ma_row[0]
            
        ma10 /= 10
        
        upper = (1 + M1/100) * ma10
        lower = (1 - M2/100) * ma10
        ene = (upper + lower) / 2
        
        if high >= upper:
            sql = "select id from focus_pool where code='" + code + "' and type_id=3 and subtype_id=1"
            cursor.execute(sql)
            upper_res = cursor.fetchone()
            if upper_res:
                sql = "update focus_pool set count=count+1, latest=%s where id=%s"
                param = (today, upper_res[0])
            else:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 3, 1, close)
                 
            cursor.execute(sql, param)
            conn.commit()
            
        if low <= lower:
            sql = "select id from focus_pool where code='" + code + "' and type_id=4 and subtype_id=1"
            cursor.execute(sql)
            lower_res = cursor.fetchone()
            if lower_res:
                sql = "update focus_pool set count=count+1, latest=%s where id=%s"
                param = (today, lower_res[0])
            else:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 4, 1, close)
                 
            cursor.execute(sql, param)
            conn.commit()
        else:   # ene最接近下轨top50
            dist_per = (low - lower) / (upper - lower)
            code_dist = (code, dist_per, close)
            
            if len(close_lower_list) < 50:
                close_lower_list.append(code_dist)
            else:
                close_lower_list = sorted(close_lower_list, key=lambda ene: ene[1])
                if close_lower_list[49][1] > dist_per:
                    close_lower_list.pop()
                    close_lower_list.append(code_dist)
            
    close_lower_list = sorted(close_lower_list, key=lambda ene: ene[1])
    for ene_tuple in close_lower_list:
        sql = "select id from focus_pool where code='" + ene_tuple[0] + "' and type_id=5 and subtype_id=1"
        cursor.execute(sql)
        close_lower_res = cursor.fetchone()
        if close_lower_res:
            sql = "update focus_pool set count=count+1, latest=%s where id=%s"
            param = (today, close_lower_res[0])
        else:
            sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
            param = (ene_tuple[0], today, 5, 1, ene_tuple[2])
            
        cursor.execute(sql, param)
        conn.commit()
        
        # 插入close_ene_lower表
        sql = "insert into close_ene_lower(code, date, dist_per) values(%s,%s,%s)"
        param = (ene_tuple[0], today, ene_tuple[1])
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