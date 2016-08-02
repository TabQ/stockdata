# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

print datetime.datetime.now()

today = str(date.today())

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    sql = "select code, max, min, direction from super_wave"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        _max = row[1]
        _min = row[2]
        _dir = row[3]
        
        sql = "select close from perday_info where code=%s and date=%s"
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
                    _max = close
                    sql = "update super_wave set percent=%s, max=%s, date=%s, cur_per=0 where code=%s"
                    param = (percent, _max, today, code)
                    
                    cursor.execute(sql, param)
                    conn.commit()
                else:
                    percent = (close - _max) / _max
                    # 判断是否发生超跌
                    if -percent >= 0.3:
                        _min = close
                        sql = "update super_wave set min=%s, percent=%s, date=%s, cur_per=0, direction=-1 where code=%s"
                        param = (_min, percent, today, code)
                        
                        cursor.execute(sql, param)
                        conn.commit()
                    else:
                        sql = "update super_wave set date=%s, cur_per=%s where code=%s"
                        param = (today, percent, code)
                        
                        cursor.execute(sql, param)
                        conn.commit()
            elif _dir == -1:        # 超跌方向        
                # 继续超跌
                if close <= _min:
                    percent = (close - _max) / _max
                    _min = close
                    sql = "update super_wave set date=%s, min=%s, percent=%s, cur_per=0 where code=%s"
                    param = (today, _min, percent, code)
                    
                    cursor.execute(sql, param)
                    conn.commit()
                else:
                    percent = (close - _min) / _min
                    # 判断是否发生超涨
                    if percent >= 0.3:
                        _max = close
                        sql = "update super_wave set max=%s, percent=%s, date=%s, cur_per=0, direction=1 where code=%s"
                        param = (_max, percent, today, code)
                        
                        cursor.execute(sql, param)
                        conn.commit()
                    else:
                        sql = "update super_wave set date=%s, cur_per=%s where code=%s"
                        param = (today, percent, code)
                        
                        cursor.execute(sql, param)
                        conn.commit()
            
cursor.close()
conn.close()

print datetime.datetime.now()