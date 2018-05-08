# -*- coding: utf-8 -*-
from __future__ import division
import tushare as ts
import MySQLdb
from datetime import date
import time
import winsound

stocks = ['000488']

today = str(date.today())
morning_start = time.mktime(time.strptime(today + ' 09:25:00', '%Y-%m-%d %H:%M:%S'))
morning_end = time.mktime(time.strptime(today + ' 11:30:00', '%Y-%m-%d %H:%M:%S'))
afternoon_start = time.mktime(time.strptime(today + ' 13:00:00', '%Y-%m-%d %H:%M:%S'))
afternoon_end = time.mktime(time.strptime(today + ' 15:00:00', '%Y-%m-%d %H:%M:%S'))
while(True):
    now = time.time()
    if now < morning_start or (now > morning_end and now < afternoon_start):
        continue
    if now > afternoon_end:
        break
    
    df = ts.get_realtime_quotes(stocks)
    if df is not None:
        for index in df.index:
            temp = df.ix[index]
            
            if temp['price']/temp['pre_close'] > 2:
                
                print temp['code'], ' ', temp['price'], ' ', temp['time']
                winsound.Beep(2000, 2000)