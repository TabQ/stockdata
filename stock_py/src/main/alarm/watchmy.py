# -*- coding: utf-8 -*-
from __future__ import division
import tushare as ts
from datetime import date
import time
import winsound
import webbrowser
import os

url1 = 'http://www.wetoco.com'
url2 = 'http://www.infodata.cc'
code_cost = {'600031':9.955,'600031':9.4,'600267':13.92,'601006':10.06}

today = str(date.today())
morning_start = time.mktime(time.strptime(today + ' 09:25:00', '%Y-%m-%d %H:%M:%S'))
morning_end = time.mktime(time.strptime(today + ' 11:30:00', '%Y-%m-%d %H:%M:%S'))
afternoon_start = time.mktime(time.strptime(today + ' 13:00:00', '%Y-%m-%d %H:%M:%S'))
afternoon_end = time.mktime(time.strptime(today + ' 15:00:00', '%Y-%m-%d %H:%M:%S'))
while(True):
    now = time.time()
    nowstr = time.strftime('%H:%M:%S', time.localtime(now))
    if now < morning_start or (now > morning_end and now < afternoon_start):
        continue
    if now > afternoon_end:
        break
    
    try:
        df = ts.get_realtime_quotes(code_cost.keys())
        if df is not None:
            for index in df.index:
                temp = df.ix[index]
                range = (float(temp['price']) - code_cost[temp['code']])*100 / code_cost[temp['code']]
                if range >= 1.0:
                    webbrowser.open(url1, 1)
                    winsound.Beep(4000, 2000)
                    print temp['code'],range
                    os._exit(0)
                elif range <= -1.0:
                    webbrowser.open(url2, 1)
                    winsound.Beep(2000, 2000)
                    print temp['code'],range
                    os._exit(0)
    except:
        pass