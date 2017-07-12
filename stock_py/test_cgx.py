# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

def test_cgx(start = '2017-01-01', end = str(date.today()), type = 'H'):
    x_axes = []
    y_axes = []
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where (calendarDate >=%s and calendarDate <= %s) and isOpen=1 order by calendarDate"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        x_axes.append(datetime.datetime.strptime(date, '%Y-%m-%d'))
        
        if type == 'H':
            sql = "select close, ma13 from k_data as k, stocks_extends as s where k.code='sh000001' and s.code='000001' and k.date=s.date and k.date=%s"
        elif type == 'S':
            sql = "select close, ma13 from k_data as k, stocks_extends as s where k.code='sz399001' and s.code='399001' and k.date=s.date and k.date=%s"
        elif type == 'Z':
            sql = "select close, ma13 from k_data as k, stocks_extends as s where k.code='sz399005' and s.code='399005' and k.date=s.date and k.date=%s"
        elif type == 'C':
            sql = "select close, ma13 from k_data as k, stocks_extends as s where k.code='sz399006' and s.code='399006' and k.date=s.date and k.date=%s"
        param = (date)
        cursor.execute(sql, param)
        result = cursor.fetchone()
            
        y_axes.append(result[0] - result[1])
            
            
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title(type);
    ax.plot(x_axes, y_axes, 'bo', x_axes, y_axes, 'K')
    ax.xaxis.set_major_locator(mdate.DayLocator(bymonthday=range(1,32), interval=1))
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()
    
    plt.show()
    
    
test_cgx(end='2017-02-17')