# -*- coding: utf-8 -*-
from __future__ import division
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

from common import diff_between_two_days, ma_date, hld
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
        
        close_lower_list = []
        
        for row in results:
            code = row[0]
            high = row[1]
            close = row[2]
            low = row[3]
            timeToMarket = row[4]
            
            if diff_between_two_days(date, timeToMarket) < 3*30:
                continue
            
            # 计算ma10
            ma10 = ma_date(cursor, code, 'S', date, 10)
            
            upper = (1 + M1/100) * ma10
            lower = (1 - M2/100) * ma10
            ene = (upper + lower) / 2
            
            if high >= upper:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, date, 2, 1, close)
                     
                cursor.execute(sql, param)
                conn.commit()
                
            if low <= lower:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, date, 3, 1, close)
                     
                cursor.execute(sql, param)
                conn.commit()
            else:   # ene最接近下轨top50
                dist_per = (low - lower) * 1.00 / (upper - lower) * 1.00
                dist_per = round(dist_per, 2)
                
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
            sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
            param = (ene_tuple[0], date, 4, 1, ene_tuple[2])
                
            cursor.execute(sql, param)
            conn.commit()
            
            # 更新或插入dist_per于stocks_extends当中
            sql = "select id from stocks_extends where code=%s and date=%s and type='S'"
            param = (ene_tuple[0], date)
            cursor.execute(sql, param)
            exists = cursor.fetchone()
            
            if exists:
                sql = "update stocks_extends set dist_per=%s where code=%s and date=%s and type='S'"
            else:
                sql = "insert into stocks_extends(dist_per, code, date, type) values(%s, %s, %s, 'S')"
                
            param = (ene_tuple[1], ene_tuple[0], date)
            cursor.execute(sql, param)
            conn.commit()
        
    cursor.close()
    conn.close()
    
    print 'ene end: ', datetime.datetime.now()
    
# 持股线距离（HLD）模型
def handle_hld(start = str(date.today()), end = str(date.today())):
    m = 10  # hld的移动平均线（ma）计算间隔
    type_id = 19 # hld的focus_type id设为19
    
    print 'handle_hld start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select code from stocks_info where type='S'"
        cursor.execute(sql)
        si_results = cursor.fetchall()
        
        for si_row in si_results:
            code = si_row[0]
            
            hld_value = hld(cursor, code, date)

            if hld_value is not None:
                sql = "insert into hld(code, date, hld) values(%s, %s, %s)"
                param = (code, date, hld_value)
                cursor.execute(sql, param)
                conn.commit()
                
                sql = "select hld from hld where code=%s and date<=%s and hld is not null order by date desc limit %s"
                param = (code, date, m)
                cursor.execute(sql, param)
                hld_results = cursor.fetchall()
                
                if len(hld_results) == m:
                    hld_list = []
                    for hld_row in hld_results:
                        hld_list.append(hld_row[0])
                        
                    mahld = ma(hld_list)
                    sql = "update hld set mahld=%s where code=%s and date=%s"
                    param = (mahld, code, date)
                    cursor.execute(sql, param)
                    conn.commit()
                    
                    if hld_value >= mahld:
                        sql = "select hld, mahld from hld where code=%s and date<%s and hld is not null and mahld is not null limit 1"
                        param = (code, date)
                        cursor.execute(sql, param)
                        prior_hld_row = cursor.fetchone()
                        
                        if prior_hld_row:
                            prior_hld = prior_hld_row[0]
                            prior_mahld = prior_hld_row[1]
                            
                            # hld金叉入库(focus_pool)
                            if prior_hld < prior_mahld:
                                sql = "select close from k_data where code=%s and date=%s and type='S'"
                                param = (code, date)
                                cursor.execute(sql, param)
                                close_row = cursor.fetchone()
                                
                                if close_row:
                                    sql = "insert into focus_pool(code, date, cost_price, type_id, subtype_id) values(%s, %s, %s, %s, %s)"
                                    param = (code, date, close_row[0], type_id, 1)
                                    cursor.execute(sql, param)
                                    conn.commit()
    
    cursor.close()
    conn.close()
    
    print 'handle_hld end: ', datetime.datetime.now()