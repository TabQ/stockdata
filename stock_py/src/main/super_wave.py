# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

from common import diff_between_two_days

def super_wave(today = str(date.today())):
    print 'super_wave start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
    cursor.execute(sql)
    dateRes = cursor.fetchone()
    
    if dateRes:
        sql = "select code, max, min, direction, cost_price, summit_date from super_wave"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            _max = row[1]
            _min = row[2]
            _dir = row[3]
            cost_price = row[4]
            summit_date= row[5]
            
            sql = "select close from k_data where code=%s and date=%s"
            param = (code, today)
            cursor.execute(sql, param)
            todayRes = cursor.fetchone()
            
            if todayRes:
                close = todayRes[0]
                
                # 超涨方向
                if _dir == 1:
                    # 继续超涨
                    if close >= _max:
                        percent = (close - _min) / _min
                        yield_rate = (close - cost_price) / cost_price
                        sql = "update super_wave set percent=%s, max=%s, summit_date=%s, yield_rate=%s, cur_per=0 where code=%s"
                        param = (percent, close, today, yield_rate, code)
                        
                        cursor.execute(sql, param)
                        conn.commit()
                    else:
                        percent = (close - _max) / _max
                        # 判断是否发生超跌
                        if -percent >= 0.3:
                            yield_rate = (close - _max) /_max
                            sql = "update super_wave set min=%s, percent=%s, summit_date=%s, cost_date=%s, cost_price=%s, yield_rate=%s, cur_per=0, direction=-1 where code=%s"
                            param = (close, percent, today, summit_date, _max, yield_rate, code)
                            
                            cursor.execute(sql, param)
                            conn.commit()
                        else:
                            yield_rate = (close - cost_price) / cost_price
                            sql = "update super_wave set cur_per=%s, yield_rate=%s where code=%s"
                            param = (percent, yield_rate, code)
                            
                            cursor.execute(sql, param)
                            conn.commit()
                elif _dir == -1:        # 超跌方向
                    # 继续超跌
                    if close <= _min:
                        percent = (close - _max) / _max
                        yield_rate = (close - cost_price) / cost_price
                        sql = "update super_wave set summit_date=%s, min=%s, percent=%s, yield_rate=%s, cur_per=0 where code=%s"
                        param = (today, close, percent, yield_rate, code)
                        
                        cursor.execute(sql, param)
                        conn.commit()
                    else:
                        percent = (close - _min) / _min
                        # 判断是否发生超涨
                        if percent >= 0.3:
                            yield_rate = (close - _min) / _min
                            sql = "update super_wave set max=%s, percent=%s, summit_date=%s, cost_date=%s, cost_price=%s, yield_rate=%s, cur_per=0, direction=1 where code=%s"
                            param = (close, percent, today, summit_date, _min, yield_rate, code)
                            
                            cursor.execute(sql, param)
                            conn.commit()
                        else:
                            yield_rate = (close - cost_price) / cost_price
                            sql = "update super_wave set cur_per=%s, yield_rate=%s where code=%s"
                            param = (percent, yield_rate, code)
                            
                            cursor.execute(sql, param)
                            conn.commit()
                
    cursor.close()
    conn.close()
    
    print 'super_wave end: ', datetime.datetime.now()
    

def super_wave_init(today = str(date.today())):
    print 'super_wave_init start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
    cursor.execute(sql)
    dateRes = cursor.fetchone()
    
    if dateRes:
        sql = "select k.code, close, timeToMarket from k_data as k, stocks_info as s where k.code=s.code and date='"+today+"'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            close = row[1]
            timeToMarket = row[2]
            
            if diff_between_two_days(today, timeToMarket) < 20:
                continue
            
            sql = "select code from super_wave where code='"+code+"'"
            cursor.execute(sql)
            swResult = cursor.fetchone()
        
            if swResult:
                continue
            
            sql = "insert into super_wave(code,cost_date,min,max,cost_price) values(%s,%s,%s,%s,%s)"
            param = (code, today, close, close, close)
            cursor.execute(sql, param)
            conn.commit()
            
    cursor.close()
    conn.close()
    
    print 'super_wave_init end: ', datetime.datetime.now()