# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

def test_yield():
    print datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where (calendarDate >='2017-01-01' and calendarDate <= '2017-02-18') and isOpen=1"
    cursor.execute(sql)
    start_results = cursor.fetchall()
    
    for start_row in start_results:
        start_date = start_row[0]
        
        sql = "select code, cost_price from focus_pool where type_id=3 and date=%s"
        param = (start_date)
        cursor.execute(sql, param)
        results = cursor.fetchall()
        
        if results:
            sum_yield = i = 0
            
            for row in results:
                code = row[0]
                cost_price = row[1]
                
                sql = "select calendarDate from trade_cal where calendarDate >= '"+start_date+"' and isOpen = 1 order by calendarDate limit 7,1"
                cursor.execute(sql)
                end_result = cursor.fetchone()
                end_date = end_result[0]
                
                sql = "select close from k_data where code=%s and date=%s"
                param = (code, end_date)
                cursor.execute(sql, param)
                sum_result = cursor.fetchone()
                
                if sum_result:
                    i = i + 1
                    close = sum_result[0]
                    sum_yield += (close - cost_price) * 1.00 / cost_price
                    
            if i > 0:
                sum_yield = sum_yield*1.00 / i
                    
            sql = "insert into test_yield(start_date, end_date, sum_yield) values(%s, %s, %s)"
            param = (start_date, end_date, sum_yield)
            cursor.execute(sql, param)
            conn.commit()
            
    print datetime.datetime.now()
    
test_yield()