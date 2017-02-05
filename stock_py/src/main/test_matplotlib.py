# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

def test_ene_yield(type = 'A'):
    y_axes = []
    x_start_axes = []
    x_end_axes = []
    cur_y = 0
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where (calendarDate >='2016-01-28' and calendarDate <= '2017-01-17') and isOpen=1"
    cursor.execute(sql)
    x_results = cursor.fetchall()
    
    for x_row in x_results:
        cal_date = x_row[0]
        x_start_axes.append(datetime.datetime.strptime(cal_date, '%Y-%m-%d'))
        
        if type == 'A':
            sql = "select start_date, end_date, sum_yield from test_yield where start_date='"+cal_date+"' and type='A'"
        elif type == 'H':
            sql = "select start_date, end_date, sum_yield from test_yield where start_date='"+cal_date+"' and type='H'"
        elif type == 'S':
            sql = "select start_date, end_date, sum_yield from test_yield where start_date='"+cal_date+"' and type='S'"
        elif type == 'C':
            sql = "select start_date, end_date, sum_yield from test_yield where start_date='"+cal_date+"' and type='C'"
        cursor.execute(sql)
        test_yield_result = cursor.fetchone()
        
        if test_yield_result:
            cur_y += test_yield_result[2]
            y_axes.append(cur_y)
            x_end_axes.append(datetime.datetime.strptime(test_yield_result[1], '%Y-%m-%d'))
        else:
            y_axes.append(cur_y)
            sql = "select calendarDate from trade_cal where calendarDate >= '"+cal_date+"' and isOpen = 1 order by calendarDate limit 7,1"
            cursor.execute(sql)
            end_result = cursor.fetchone()
            x_end_axes.append(datetime.datetime.strptime(end_result[0], '%Y-%m-%d'))
            
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(x_end_axes, y_axes)
    ax.xaxis.set_major_locator(mdate.DayLocator(bymonthday=range(1,32), interval=15))
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()
    
    plt.show()
    
test_ene_yield('C')