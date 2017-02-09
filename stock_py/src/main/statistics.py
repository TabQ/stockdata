# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import traceback
import sys

from common import diff_between_two_days, ma_date, max_ma_vol_date, max_vol_price

# 处理所有股票的最大成交量及最高收盘价
def handle_max_vol_price():
    print 'handle_max_vol_price start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select code,type from stocks_info"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        type = row[1]
        
        max_vol_price_tuple = max_vol_price(cursor, code, type)
        max_vol = max_vol_price_tuple[0]
        max_price = max_vol_price_tuple[1]
        
        sql = "select id from stocks_summit where code=%s and type=%s"
        param = (code, type)
        cursor.execute(sql, param)
        exists = cursor.fetchone()
        
        if exists:
            sql = "update stocks_summit set max_vol=%s, max_price=%s where code=%s and type=%s"
        else:
            sql = "insert into stocks_summit(max_vol, max_price, code, type) values(%s, %s, %s, %s)"
            
        param = (max_vol, max_price, code, type)
        cursor.execute(sql, param)
        conn.commit()
        
    cursor.close()
    conn.close()
    
    print 'handle_max_vol_price end: ', datetime.datetime.now()

# 处理所有股票某个时间段的几条重要最大成交量及均量
def handle_max_ma_vol(start = str(date.today()), end = str(date.today())):
    print 'handle_max_ma_vol start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    days_list = [5, 10, 20, 60, 120]
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    for row in results:
        date = row[0]
        
        sql = "select code,type from stocks_info"
        cursor.execute(sql)
        codes_results = cursor.fetchall()
        for codes_row in codes_results:
            code = codes_row[0]
            type = codes_row[1]
            
            for n in days_list:
                max_ma = max_ma_vol_date(cursor, code, type, date, n)
                
                if max_ma == -1:
                    continue
                else:
                    max = max_ma[0]
                    ma  = max_ma[1]
                    
                    sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
                    param = (code, date, type)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    if exists:
                        if n == 5:
                            sql = "update stocks_extends set v_ma5=%s, max_vol5=%s where id=%s"
                        elif n == 10:
                            sql = "update stocks_extends set v_ma10=%s, max_vol10=%s where id=%s"
                        elif n == 20:
                            sql = "update stocks_extends set v_ma20=%s, max_vol20=%s where id=%s"
                        elif n == 60:
                            sql = "update stocks_extends set v_ma60=%s, max_vol60=%s where id=%s"
                        elif n == 120:
                            sql = "update stocks_extends set v_ma120=%s, max_vol120=%s where id=%s"
                         
                        param = (ma, max, exists[0])
                    else:
                        if n == 5:
                            sql = "insert into stocks_extends(code, date, type, v_ma5, max_vol5) values(%s, %s, %s, %s, %s)"
                        elif n == 10:
                            sql = "insert into stocks_extends(code, date, type, v_ma10, max_vol10) values(%s, %s, %s, %s, %s)"
                        elif n == 20:
                            sql = "insert into stocks_extends(code, date, type, v_ma20, max_vol20) values(%s, %s, %s, %s, %s)"
                        elif n == 60:
                            sql = "insert into stocks_extends(code, date, type, v_ma60, max_vol60) values(%s, %s, %s, %s, %s)"
                        elif n == 120:
                            sql = "insert into stocks_extends(code, date, type, v_ma120, max_vol120) values(%s, %s, %s, %s, %s)"
                             
                        param = (code, date, type, ma, max)
                        
                    cursor.execute(sql, param)
                    conn.commit()
                    
    cursor.close()
    conn.close()
    
    print 'handle_max_ma_vol end: ', datetime.datetime.now()

# 处理某个时间段的所有股票的移动平均线
def handle_ma(start = str(date.today()), end = str(date.today())):
    print 'handle_ma start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    days_list = [5, 10, 13, 14, 15, 20, 60, 120, 250]
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    for row in results:
        date = row[0]
        
        sql = "select code, type from stocks_info"
        cursor.execute(sql)
        codes_results = cursor.fetchall()
        for codes_row in codes_results:
            code = codes_row[0]
            type = codes_row[1]
            
            for n in days_list:
                ma_now = ma_date(cursor, code, type, date, n)
                if ma_now < 0:
                    continue
                else:
                    sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
                    param = (code, date, type)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    
                    if exists:
                        if n == 5:
                            sql = "update stocks_extends set ma5=%s where code=%s and date=%s and type=%s"
                        elif n == 10:
                            sql = "update stocks_extends set ma10=%s where code=%s and date=%s and type=%s"
                        elif n == 13:
                            sql = "update stocks_extends set ma13=%s where code=%s and date=%s and type=%s"
                        elif n == 14:
                            sql = "update stocks_extends set ma14=%s where code=%s and date=%s and type=%s"
                        elif n == 15:
                            sql = "update stocks_extends set ma15=%s where code=%s and date=%s and type=%s"
                        elif n == 20:
                            sql = "update stocks_extends set ma20=%s where code=%s and date=%s and type=%s"
                        elif n == 60:
                            sql = "update stocks_extends set ma60=%s where code=%s and date=%s and type=%s"
                        elif n == 120:
                            sql = "update stocks_extends set ma120=%s where code=%s and date=%s and type=%s"
                        elif n == 250:
                            sql = "update stocks_extends set ma250=%s where code=%s and date=%s and type=%s"
                    else:
                        if n == 5:
                            sql = "insert into stocks_extends(ma5,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 10:
                            sql = "insert into stocks_extends(ma10,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 13:
                            sql = "insert into stocks_extends(ma13,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 14:
                            sql = "insert into stocks_extends(ma14,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 15:
                            sql = "insert into stocks_extends(ma15,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 20:
                            sql = "insert into stocks_extends(ma20,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 60:
                            sql = "insert into stocks_extends(ma60,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 120:
                            sql = "insert into stocks_extends(ma120,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 250:
                            sql = "insert into stocks_extends(ma250,code,date,type) values(%s,%s,%s,%s)"
                            
                    param = (ma_now, code, date, type)
                    cursor.execute(sql, param)
                    conn.commit()
                
    cursor.close()
    conn.close()
    
    print 'handle_ma end: ', datetime.datetime.now()

# 计算每日涨跌幅
def p_change(start = str(date.today()), end = str(date.today())):
    print 'p_change start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select code,type from stocks_info"
    
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        type = row[1]
    
        sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
        param = (start, end)
        cursor.execute(sql, param)
        results = cursor.fetchall()
        
        for row in results:
            date = row[0]
            
            sql = "select close, date from k_data where code=%s and type=%s and date<=%s order by date desc limit 2"
            param = (code, type, date)
            cursor.execute(sql, param)
            close_results =  cursor.fetchall()
            
            count = 0
            close_list = []
            for close_row in close_results:
                close = close_row[0]
                now = close_row[1]
                
                if count == 0 and now != date:
                    break

                count += 1                
                close_list.append(close)
                
            if len(close_list) != 2:
                continue
            else:
                p_change = (close_list[0] - close_list[1]) * 100.00 / close_list[1]
                p_change = round(p_change, 2)
            
            sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
            param = (code, date, type)
            cursor.execute(sql, param)
            exists = cursor.fetchone()
            
            if exists:
                sql = "update stocks_extends set p_change=%s where code=%s and date=%s and type=%s"
            else:
                sql = "insert into stocks_extends(p_change, code, date, type) values(%s, %s, %s, %s)"
                
            param = (p_change, code, date, type)
            cursor.execute(sql, param)
            conn.commit()
    
    cursor.close()
    conn.close()
    
    print 'p_change end: ', datetime.datetime.now()
    
# 计算关注池收益率
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
    
# 成交量相关计算（突破，缩量）
def volume(start = str(date.today()), end = str(date.today())):
    print 'volume start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    for row in results:
        date = row[0]
        
        sql = "select code, timeToMarket from stocks_info where type='S'"
        cursor.execute(sql)
        codes_results = cursor.fetchall()
        
        for code_row in codes_results:
            code = code_row[0]
            timeToMarket = code_row[1]
            
            if diff_between_two_days(date, timeToMarket) < 3*30:
                continue
            
            sql = "select volume from k_data where code=%s and date=%s and type='S'"
            param = (code, date)
            cursor.execute(sql, param)
            vol_result = cursor.fetchone()
            
            if vol_result:
                volume = vol_result[0]
            else:
                continue
            
            sql = "select v_ma5,v_ma10,v_ma20,v_ma60,v_ma120,max_vol5,max_vol10,max_vol20,max_vol60,max_vol120 from stocks_extends where code=%s and date=%s and type='S'"
            param = (code, date)
            cursor.execute(sql, param)
            extends_result = cursor.fetchone()
            
            if extends_result:
                v_ma5       = extends_result[0]
                v_ma10      = extends_result[1]
                v_ma20      = extends_result[2]
                v_ma60      = extends_result[3]
                v_ma120     = extends_result[4]
                max_vol5    = extends_result[5]
                max_vol10   = extends_result[6]
                max_vol20   = extends_result[7]
                max_vol60   = extends_result[8]
                max_vol120  = extends_result[9]
                
                vol_break_5d = vol_break_10d = vol_break_20d = 0
                vol_shrink_ma_5d = vol_shrink_ma_10d = vol_shrink_ma_20d = vol_shrink_ma_60d = vol_shrink_ma_120d = 0
                vol_shrink_max_5d = vol_shrink_max_10d = vol_shrink_max_20d = vol_shrink_max_60d = vol_shrink_max_120d = 0
                
                if v_ma5 != 0:
                    vol_break_5d = vol_shrink_ma_5d = round(volume / v_ma5, 2)
                if v_ma10 != 0:
                    vol_break_10d = vol_shrink_ma_10d = round(volume / v_ma10, 2)
                if v_ma20 != 0:
                    vol_break_20d = vol_shrink_ma_20d = round(volume / v_ma20, 2)
                if v_ma60 != 0:
                    vol_shrink_ma_60d = round(volume / v_ma60, 2)
                if v_ma120 != 0:
                    vol_shrink_ma_120d = round(volume / v_ma120, 2)
                if max_vol5 != 0:
                    vol_shrink_max_5d = round(volume / max_vol5, 2)
                if max_vol10 != 0:
                    vol_shrink_max_10d = round(volume / max_vol10, 2)
                if max_vol20 != 0:
                    vol_shrink_max_20d = round(volume / max_vol20, 2)
                if max_vol60 != 0:
                    vol_shrink_max_60d = round(volume / max_vol60, 2)
                if max_vol120 != 0:
                    vol_shrink_max_120d = round(volume / max_vol120, 2)
                    
                sql = "select id from volume where code=%s and date=%s"
                param = (code, date)
                cursor.execute(sql, param)
                exists = cursor.fetchone()
                
                if exists:
                    sql = '''update volume set vol_break_5d=%s, vol_break_10d=%s, vol_break_20d=%s, vol_shrink_max_5d=%s, vol_shrink_max_10d=%s, vol_shrink_max_20d=%s, 
                    vol_shrink_max_60d=%s, vol_shrink_max_120d=%s, vol_shrink_ma_5d=%s, vol_shrink_ma_10d=%s, vol_shrink_ma_20d=%s, vol_shrink_ma_60d=%s, vol_shrink_ma_120d=%s 
                    where code=%s and date=%s'''
                else:
                    sql = '''insert into volume(vol_break_5d, vol_break_10d, vol_break_20d, vol_shrink_max_5d, vol_shrink_max_10d, vol_shrink_max_20d, 
                    vol_shrink_max_60d, vol_shrink_max_120d, vol_shrink_ma_5d, vol_shrink_ma_10d, vol_shrink_ma_20d, vol_shrink_ma_60d, vol_shrink_ma_120d, code, date) 
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    
                param = (vol_break_5d, vol_break_10d, vol_break_20d, vol_shrink_max_5d, vol_shrink_max_10d, vol_shrink_max_20d, vol_shrink_max_60d, vol_shrink_max_120d,\
                         vol_shrink_ma_5d, vol_shrink_ma_10d, vol_shrink_ma_20d, vol_shrink_ma_60d, vol_shrink_ma_120d, code, date)
                cursor.execute(sql, param)
                conn.commit()
            
            sql = "select max_vol from stocks_summit where code=%s and type='S'"
            param = (code)
            cursor.execute(sql, param)
            max_vol_result = cursor.fetchone()
            
            if max_vol_result:
                max_vol = max_vol_result[0]
                
                if max_vol != 0:
                    vol_shrink_max = round(volume / max_vol, 2)
                    
                    sql = "select id from volume where code=%s and date=%s"
                    param = (code, date)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    
                    if exists:
                        sql = "update volume set vol_shrink_max=%s where code=%s and date=%s"
                    else:
                        sql = "insert into volume(vol_shrink_max, code, date) volues(%s, %s, %s)"
                        
                    param = (vol_shrink_max, code, date)
                    cursor.execute(sql, param)
                    conn.commit()
    
    print 'volume end: ', datetime.datetime.now()
    