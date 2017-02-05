# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

from common import diff_between_two_days

def volume_break(today = str(date.today())):
    print 'volume_break start: ', datetime.datetime.now()
    
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
                sql = "insert into focus_pool(code,date,type_id,subtype_id,cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 2, 1, close)
                cursor.execute(sql, param)
                conn.commit()
                    
                sql = "insert into volume_break(code,date,v2ma5) values(%s,%s,%s)"
                param = (code, today, v2ma5)
                cursor.execute(sql, param)
                conn.commit()
            elif v2ma20 >= 2.0:
                sql = "insert into focus_pool(code,date,type_id,subtype_id,cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 6, 1, close)
                cursor.execute(sql, param)
                conn.commit()
                    
                sql = "insert into volume_break(code,date,v2ma20) values(%s,%s,%s)"
                param = (code, today, v2ma20)
                cursor.execute(sql, param)
                conn.commit()
    
    cursor.close()
    conn.close()
    
    print 'volume_break end: ', datetime.datetime.now()

def ene(today = str(date.today())):
    # ENE公式：N:=10;M1:=11;M2:=9;
    # UPPER:(1+M1/100)*MA(CLOSE,N);
    # LOWER:(1-M2/100)*MA(CLOSE,N);
    # ENE:(UPPER+LOWER)/2;
    
    N = 10.00
    M1 = 11.00
    M2 = 9.00
    
    print 'ene start: ', datetime.datetime.now()
    
    # today = '2016-11-29'
    
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
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 3, 1, close)
                     
                cursor.execute(sql, param)
                conn.commit()
                
            if low <= lower:
                sql = "insert into focus_pool(code, date, type_id, subtype_id, cost_price) values(%s,%s,%s,%s,%s)"
                param = (code, today, 4, 1, close)
                     
                cursor.execute(sql, param)
                conn.commit()
            else:   # ene最接近下轨top50
                dist_per = (low - lower) * 1.00 / (upper - lower) * 1.00
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
    
    print 'ene end: ', datetime.datetime.now()