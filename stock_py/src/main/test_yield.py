# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

def test_yield(type = 'A'):
    print datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where (calendarDate >='2017-02-09' and calendarDate <= '2017-02-15') and isOpen=1"
    cursor.execute(sql)
    start_results = cursor.fetchall()
    
    for start_row in start_results:
        start_date = start_row[0]
        
        if type == 'A':
            sql = "select code, cost_price from focus_pool where type_id=3 and date='" + start_date + "'"
        elif type == 'H':
            sql = "select code, cost_price from focus_pool where type_id=3 and date='" + start_date + "' and code like '60%'"
        elif type == 'S':
            sql = "select code, cost_price from focus_pool where type_id=3 and date='" + start_date + "' and code like '000%'"
        elif type == 'Z':
            sql = "select code, cost_price from focus_pool where type_id=3 and date='" + start_date + "' and code like '002%'"
        elif type == 'C':
            sql = "select code, cost_price from focus_pool where type_id=3 and date='" + start_date + "' and code like '300%'"
            
        cursor.execute(sql)
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
                    
            if type == 'A':
                sql = "insert into test_yield(start_date, end_date, sum_yield, type) values(%s, %s, %s, 'A')"
            elif type == 'H':
                sql = "insert into test_yield(start_date, end_date, sum_yield, type) values(%s, %s, %s, 'H')"
            elif type == 'S':
                sql = "insert into test_yield(start_date, end_date, sum_yield, type) values(%s, %s, %s, 'S')"
            elif type == 'Z':
                sql = "insert into test_yield(start_date, end_date, sum_yield, type) values(%s, %s, %s, 'Z')"
            elif type == 'C':
                sql = "insert into test_yield(start_date, end_date, sum_yield, type) values(%s, %s, %s, 'C')"
            param = (start_date, end_date, sum_yield)
            cursor.execute(sql, param)
            conn.commit()
            
    print datetime.datetime.now()
    
test_yield('A')
test_yield('H')
test_yield('S')
test_yield('Z')
test_yield('C')