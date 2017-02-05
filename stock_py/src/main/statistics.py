# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import traceback
import sys

from common import diff_between_two_days

def stocks_extends(today = str(date.today())):
    print 'stocks_extends start: ', datetime.datetime.now()
    
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
    
    print 'stocks_extends end: ', datetime.datetime.now()
    

def focus_pool_rate(today = str(date.today())):
    print 'focus_pool_rate start: ', datetime.datetime.now()
    
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
    
    print 'focus_pool_rate end: ', datetime.datetime.now()
    

def up_down(today = str(date.today())):
    print 'up_down start: ', datetime.datetime.now()
    
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
    
    print 'up_down end: ', datetime.datetime.now()