# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

def diff_between_two_days(day1, day2):
    if day1 == '0' or day2 == '0':
        return 0
    if day1 == '' or day2 == '':
        return 0
    
    second1 = datetime.datetime.strptime(day1, "%Y-%m-%d")
    second1 = time.mktime(second1.timetuple())
    
    second2 = datetime.datetime.strptime(day2, "%Y-%m-%d")
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
    
    sql = "select code, cost_price, id, date from focus_pool where date < '" + today + "'"
    cursor.execute(sql)
    fpRes = cursor.fetchall()
    
    for fpRow in fpRes:
        code = fpRow[0]
        cost_price = fpRow[1]
        fp_id = fpRow[2]
        date = fpRow[3]
        
        sql = "select close from k_data where code=%s and date=%s"
        param = (code, today)
        cursor.execute(sql, param)
        k_data = cursor.fetchone()
        if k_data:
            yield_rate = (k_data[0] - cost_price) * 100.00 / cost_price
            sql = "update focus_pool set yield_rate=%s where id=%s"
            param = (yield_rate, fp_id)
            cursor.execute(sql, param)
            conn.commit()
            
            # 计算近3天收益率上升最快
            sql = "select close, date from k_data where code=%s order by date desc limit 3, 1"
            param = (code)
            cursor.execute(sql, param)
            rec3_row = cursor.fetchone()
            if rec3_row:
                if rec3_row[1] > date:
                    rec3minus = (k_data[0] - rec3_row[0]) * 100.00 / cost_price
                else:
                    rec3minus = 0.00
            # 计算近5天收益率上升最快
            sql = "select close, date from k_data where code=%s order by date desc limit 5, 1"
            param = (code)
            cursor.execute(sql, param)
            rec5_row = cursor.fetchone()
            if rec5_row:
                if rec5_row[1] > date: 
                    rec5minus = (k_data[0] - rec5_row[0]) * 100.00 / cost_price
                else:
                    rec5minus = 0.00
            # 更新rec3minus、rec5minus        
            sql = "update focus_pool set rec3minus=%s, rec5minus=%s where id=%s"
            param = (rec3minus, rec5minus, fp_id)
            cursor.execute(sql, param)
            conn.commit()
    
    # 统计最近3天收益率上升最快的top10
    sql = "select id, rec3topsdate from focus_pool where rec3minus > 0.00 order by rec3minus desc limit 10"
    cursor.execute(sql)
    rec3_res = cursor.fetchall()
    for rec3_row in rec3_res:
        rec3_id = rec3_row[0]
        rec3tops_date = rec3_row[1]
        
        if diff_between_two_days(today, rec3tops_date) > 30:
            sql = "update focus_pool set rec3tops=1, rec3topsdate=%s where id=%s"
        else:
            sql = "update focus_pool set rec3tops=rec3tops+1, rec3topsdate=%s where id=%s"
            
        param = (today, rec3_id)
        cursor.execute(sql, param)
        conn.commit()
        
    # 统计最近5天收益率上升最快的    
    sql = "select id, rec5topsdate from focus_pool where rec5minus > 0.00 order by rec5minus desc limit 10"
    cursor.execute(sql)
    rec5_res = cursor.fetchall()
    for rec5_row in rec5_res:
        rec5_id = rec5_row[0]
        rec5tops_date = rec5_row[1]
        
        if diff_between_two_days(today, rec5tops_date) > 30:
            sql = "update focus_pool set rec5tops=1, rec5topsdate=%s where id=%s"
        else:
            sql = "update focus_pool set rec5tops=rec5tops+1, rec5topsdate=%s where id=%s"
            
        param = (today, rec5_id)
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