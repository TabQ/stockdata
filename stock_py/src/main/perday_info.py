# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

print datetime.datetime.now()

today = str(date.today())

# today = '2016-02-01'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    today = dateRes[0]

    # perday_info入库开始־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (9, now)
    cursor.execute(sql, param)
    conn.commit()
    
    sql = "select code, maxVol, minPrice from stocks_info"
    
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        maxVol = row[1]
        minPrice = row[2]
            
        df = ts.get_hist_data(code, start=today, end=today)
        if df is not None:
            if today in df.index:
                df_arr = df.ix[today]
                
                _open = df_arr['open']
                high = df_arr['high']
                close = df_arr['close']
                low = df_arr['low']
                volume = df_arr['volume']
                price_change = df_arr['price_change']
                p_change = df_arr['p_change']
                ma5 = df_arr['ma5']
                ma10 = df_arr['ma10']
                ma20 = df_arr['ma20']
                v_ma5 = df_arr['v_ma5']
                v_ma10 = df_arr['v_ma10']
                v_ma20 = df_arr['v_ma20']
                turnover = df_arr['turnover']
                
                if ma20 != 0:
                    p2ma20 = close / ma20
                else:
                    p2ma20 = 0
                    
                if minPrice != 0:
                    p2min = close / minPrice
                    ma20_2_min = ma20 / minPrice
                else:
                    p2min = ma20_2_min = 0
                    
                if v_ma20 != 0:
                    v2ma20 = volume / v_ma20
                else:
                    v2ma20 = 0
                    
                if maxVol != 0:
                    v2max = volume / maxVol
                    vma20_2_max = v_ma20 / maxVol
                else:
                    v2max = vma20_2_max = 0
                
                sql = "insert into perday_info(code,date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover,\
                p2ma20,p2min,ma20_2_min,v2ma20,v2max,vma20_2_max) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (code,today,_open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover,p2ma20,p2min,ma20_2_min,v2ma20,v2max,vma20_2_max)
                cursor.execute(sql, param)
                conn.commit()
                
    # perday_info入库结束־
    now = time.time()
    sql = "insert into action_log(action_id, time) values(%s, %s)"
    param = (10, now)
    cursor.execute(sql, param)
    conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()