# -*- coding: utf-8 -*-
from __future__ import division
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

from common import diff_between_two_days, ma_date
from functions import ma, ema

def volume_break(start = str(date.today()), end = str(date.today())):
    focus_type_map = {'vol_break_5d':5, 'vol_break_10d':6, 'vol_break_20d':7}
    
    print 'volume_break start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select v.code,close,timeToMarket,v2ma5d,v2ma10d,v2ma20d from volume as v, stocks_info as s, k_data as k \
        where s.type='S' and s.code=v.code and v.code=k.code and v.date=k.date and v.date=%s"
        param = (date)
        cursor.execute(sql, param)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            close = row[1]
            timeToMarket = row[2]
            vol_break_5d = row[3]
            vol_break_10d = row[4]
            vol_break_20d = row[5]
            
            if diff_between_two_days(date, timeToMarket) < 3*30:
                continue
    
            sql = "insert into focus_pool(code, date, cost_price, type_id, subtype_id) values(%s, %s, %s, %s, %s)"
            if vol_break_5d > 2.0:
                param = (code, date, close, focus_type_map['vol_break_5d'], 1)
            elif vol_break_10d > 2.0:
                param = (code, date, close, focus_type_map['vol_break_10d'], 1)
            elif vol_break_20d > 2.0:
                param = (code, date, close, focus_type_map['vol_break_20d'], 1)
            else:
                continue
            cursor.execute(sql, param)
            conn.commit()
            
    cursor.close()
    conn.close()
        
    print 'volume_break end: ', datetime.datetime.now()
        
def ene(start = str(date.today()), end = str(date.today())):
    # ENE公式：N:=10;M1:=11;M2:=9;
    # UPPER:(1+M1/100)*MA(CLOSE,N);
    # LOWER:(1-M2/100)*MA(CLOSE,N);
    # ENE:(UPPER+LOWER)/2;
    
    N = 10.00
    M1 = 11.00
    M2 = 9.00
    
    print 'ene start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select k.code, high, close, low, timeToMarket from k_data as k, stocks_info as s where s.type='S' and k.code=s.code and date=%s"
        param = (date)
        cursor.execute(sql, param)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            high = row[1]
            close = row[2]
            low = row[3]
            timeToMarket = row[4]
            
            if diff_between_two_days(date, timeToMarket) < 20:
                continue
            
            # 计算ma10
            ma10 = ma_date(cursor, code, 'S', date, N)
            
            upper = (1 + M1/100) * ma10
            lower = (1 - M2/100) * ma10
            ene = (upper + lower) / 2
            dist = upper - lower    # ene轨道距离
            
            # 计算最高价与ene上轨的距离与轨道间距的百分比
            upper_dist_per = round((high - upper) / dist, 2)            
            if high >= upper:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, date, 2, 1, close)
                     
                cursor.execute(sql, param)
                conn.commit()
            
            # 计算最低价与ene下轨的距离与轨道间距的百分比
            lower_dist_per = round((low - lower) / dist, 2)   
            if low <= lower:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, date, 3, 1, close)
                     
                cursor.execute(sql, param)
                conn.commit()
            
            # 更新或插入upper_dist_per、lower_dist_per于stocks_extends当中
            sql = "select id from stocks_extends where code=%s and date=%s and type='S'"
            param = (code, date)
            cursor.execute(sql, param)
            exists = cursor.fetchone()
            
            if exists:
                sql = "update stocks_extends set upper_dist_per=%s, lower_dist_per=%s where code=%s and date=%s and type='S'"
            else:
                sql = "insert into stocks_extends(upper_dist_per, lower_dist_per, code, date, type) values(%s, %s, %s, %s, 'S')"
            
            param = (upper_dist_per, lower_dist_per, code, date)
            cursor.execute(sql, param)
            conn.commit()
        
    cursor.close()
    conn.close()
    
    print 'ene end: ', datetime.datetime.now()
    
# 接近ene下轨top50
def handle_close_ene_lower(start = str(date.today()), end = str(date.today())):
    print 'handle_close_ene_lower start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select s.code, close from stocks_extends s, k_data k where lower_dist_per>0 and s.type='S' and s.date=%s and s.type=k.type and s.date=k.date and s.code=k.code order by lower_dist_per limit 50"
        param = (date)
        cursor.execute(sql, param)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            cost_price = row[1]
            
            sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s, %s, %s, %s, %s)"
            param = (code, date, 4, 1, cost_price)
            cursor.execute(sql, param)
            conn.commit()
            
    cursor.close()
    conn.close()
    
    print 'handle_close_ene_lower end: ', datetime.datetime.now()
    
# 二次涨停选股法
def second_limitup(start = str(date.today()), end = str(date.today())):
    print 'second_limitup start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select code, high, low from k_data where type='S' and date=%s and close=high"
        param = (date)
        cursor.execute(sql, param)
        close_high_results = cursor.fetchall()
        
        for close_high_row in close_high_results:
            code = close_high_row[0]
            high = close_high_row[1]
            low = close_high_row[2]
            
            sql = "select close from k_data where type='S' and code=%s and date<%s order by date desc limit 1"
            param = (code, date)
            cursor.execute(sql, param)
            pre_row = cursor.fetchone()
            
            if pre_row:
                if (high - pre_row[0]) / pre_row[0] < 0.099:
                    continue
                
            sql = "select date, high, low, close from k_data where type='S' and code=%s and date<%s and close=high order by date desc limit 59"
            param = (code, date)
            cursor.execute(sql, param)
            his_results = cursor.fetchall()
            
            for his_row in his_results:
                his_date = his_row[0]
                his_high = his_row[1]
                his_low = his_row[2]
                his_close = his_row[3]
                
                if his_high != his_close:
                    continue
                
                sql = "select close from k_data where type='S' and code=%s and date<%s order by date desc limit 1"
                param = (code, his_date)
                cursor.execute(sql, param)
                his_pre_row = cursor.fetchone()
                
                if his_pre_row:
                    if (his_close - his_pre_row[0]) / his_pre_row[0] < 0.099:
                        continue
                    
                if low >= his_high or high <= his_low:
                    continue
                elif low >= his_low:
                    if his_high < high:
                        if (his_high - low) / (high - low) >= 0.5:
                            print code, ' ', date, ' ', his_date
                    else:
                        print code, ' ', date, ' ', his_date
                elif his_low >= low:
                    if high < his_high:
                        if (high - his_low) / (high - low) >= 0.5:
                            print code, ' ', date, ' ', his_date
                    else:
                        if (his_high - his_low) / (high - low) >= 0.5:
                            print code, ' ', date, ' ', his_date           
        
    cursor.close()
    conn.close()
    
    print 'second_limitup end: ', datetime.datetime.now()