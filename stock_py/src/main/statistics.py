# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import traceback
import sys

from common import diff_between_two_days, ma_date, max_ma_vol_date, max_vol_price

# 处理所有股票的最大成交量及最高收盘价
def handle_max_vol_price():
    print 'handle_max_vol_price start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select code,type from stocks_info"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        code = row[0]
        type = row[1]
        
        max_vol_price_tuple = max_vol_price(cursor, code, type)
        max_vol = max_vol_price_tuple[0]
        max_price = max_vol_price_tuple[1]
        
        sql = "select id from stocks_summit where code=%s and type=%s"
        param = (code, type)
        cursor.execute(sql, param)
        exists = cursor.fetchone()
        
        if exists:
            sql = "update stocks_summit set max_vol=%s, max_price=%s where code=%s and type=%s"
        else:
            sql = "insert into stocks_summit(max_vol, max_price, code, type) values(%s, %s, %s, %s)"
            
        param = (max_vol, max_price, code, type)
        cursor.execute(sql, param)
        conn.commit()
        
    cursor.close()
    conn.close()
    
    print 'handle_max_vol_price end: ', datetime.datetime.now()

# 处理所有股票某个时间段的几条重要最大成交量及均量
def handle_max_ma_vol(start = str(date.today()), end = str(date.today())):
    print 'handle_max_ma_vol start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    days_list = [5, 10, 20, 60, 120]
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    for row in results:
        date = row[0]
        
        sql = "select code,type from stocks_info"
        cursor.execute(sql)
        codes_results = cursor.fetchall()
        for codes_row in codes_results:
            code = codes_row[0]
            type = codes_row[1]
            
            for n in days_list:
                max_ma = max_ma_vol_date(cursor, code, type, date, n)
                
                if max_ma == -1:
                    continue
                else:
                    max = max_ma[0]
                    ma  = max_ma[1]
                    
                    sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
                    param = (code, date, type)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    if exists:
                        if n == 5:
                            sql = "update stocks_extends set v_ma5=%s, max_vol5=%s where id=%s"
                        elif n == 10:
                            sql = "update stocks_extends set v_ma10=%s, max_vol10=%s where id=%s"
                        elif n == 20:
                            sql = "update stocks_extends set v_ma20=%s, max_vol20=%s where id=%s"
                        elif n == 60:
                            sql = "update stocks_extends set v_ma60=%s, max_vol60=%s where id=%s"
                        elif n == 120:
                            sql = "update stocks_extends set v_ma120=%s, max_vol120=%s where id=%s"
                         
                        param = (ma, max, exists[0])
                    else:
                        if n == 5:
                            sql = "insert into stocks_extends(code, date, type, v_ma5, max_vol5) values(%s, %s, %s, %s, %s)"
                        elif n == 10:
                            sql = "insert into stocks_extends(code, date, type, v_ma10, max_vol10) values(%s, %s, %s, %s, %s)"
                        elif n == 20:
                            sql = "insert into stocks_extends(code, date, type, v_ma20, max_vol20) values(%s, %s, %s, %s, %s)"
                        elif n == 60:
                            sql = "insert into stocks_extends(code, date, type, v_ma60, max_vol60) values(%s, %s, %s, %s, %s)"
                        elif n == 120:
                            sql = "insert into stocks_extends(code, date, type, v_ma120, max_vol120) values(%s, %s, %s, %s, %s)"
                             
                        param = (code, date, type, ma, max)
                        
                    cursor.execute(sql, param)
                    conn.commit()
                    
    cursor.close()
    conn.close()
    
    print 'handle_max_ma_vol end: ', datetime.datetime.now()

# 处理某个时间段的所有股票的移动平均线
def handle_ma(start = str(date.today()), end = str(date.today())):
    print 'handle_ma start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    days_list = [5, 10, 13, 14, 15, 20, 60, 120, 250]
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    for row in results:
        date = row[0]
        
        sql = "select code, type from stocks_info"
        cursor.execute(sql)
        codes_results = cursor.fetchall()
        for codes_row in codes_results:
            code = codes_row[0]
            type = codes_row[1]
            
            for n in days_list:
                ma_now = ma_date(cursor, code, type, date, n)
                if ma_now < 0:
                    continue
                else:
                    sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
                    param = (code, date, type)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    
                    if exists:
                        if n == 5:
                            sql = "update stocks_extends set ma5=%s where code=%s and date=%s and type=%s"
                        elif n == 10:
                            sql = "update stocks_extends set ma10=%s where code=%s and date=%s and type=%s"
                        elif n == 13:
                            sql = "update stocks_extends set ma13=%s where code=%s and date=%s and type=%s"
                        elif n == 14:
                            sql = "update stocks_extends set ma14=%s where code=%s and date=%s and type=%s"
                        elif n == 15:
                            sql = "update stocks_extends set ma15=%s where code=%s and date=%s and type=%s"
                        elif n == 20:
                            sql = "update stocks_extends set ma20=%s where code=%s and date=%s and type=%s"
                        elif n == 60:
                            sql = "update stocks_extends set ma60=%s where code=%s and date=%s and type=%s"
                        elif n == 120:
                            sql = "update stocks_extends set ma120=%s where code=%s and date=%s and type=%s"
                        elif n == 250:
                            sql = "update stocks_extends set ma250=%s where code=%s and date=%s and type=%s"
                    else:
                        if n == 5:
                            sql = "insert into stocks_extends(ma5,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 10:
                            sql = "insert into stocks_extends(ma10,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 13:
                            sql = "insert into stocks_extends(ma13,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 14:
                            sql = "insert into stocks_extends(ma14,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 15:
                            sql = "insert into stocks_extends(ma15,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 20:
                            sql = "insert into stocks_extends(ma20,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 60:
                            sql = "insert into stocks_extends(ma60,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 120:
                            sql = "insert into stocks_extends(ma120,code,date,type) values(%s,%s,%s,%s)"
                        elif n == 250:
                            sql = "insert into stocks_extends(ma250,code,date,type) values(%s,%s,%s,%s)"
                            
                    param = (ma_now, code, date, type)
                    cursor.execute(sql, param)
                    conn.commit()
                
    cursor.close()
    conn.close()
    
    print 'handle_ma end: ', datetime.datetime.now()

# 计算每日涨跌幅
def p_change(start = str(date.today()), end = str(date.today())):
    print 'p_change start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select code,type from stocks_info"
    
    cursor.execute(sql)
    codes_results = cursor.fetchall()
    
    for code_row in codes_results:
        code = code_row[0]
        type = code_row[1]
    
        sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
        param = (start, end)
        cursor.execute(sql, param)
        cal_results = cursor.fetchall()
        
        for cal_row in cal_results:
            date = cal_row[0]
            
            sql = "select close, date from k_data where code=%s and type=%s and date<=%s order by date desc limit 2"
            param = (code, type, date)
            cursor.execute(sql, param)
            close_results =  cursor.fetchall()
            
            count = 0
            close_list = []
            for close_row in close_results:
                close = close_row[0]
                now = close_row[1]
                
                if count == 0 and now != date:
                    break

                count += 1                
                close_list.append(close)
                
            if len(close_list) != 2:
                continue
            else:
                p_change = (close_list[0] - close_list[1]) * 100.00 / close_list[1]
                p_change = round(p_change, 2)
            
            sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
            param = (code, date, type)
            cursor.execute(sql, param)
            exists = cursor.fetchone()
            
            if exists:
                sql = "update stocks_extends set p_change=%s where code=%s and date=%s and type=%s"
            else:
                sql = "insert into stocks_extends(p_change, code, date, type) values(%s, %s, %s, %s)"
                
            param = (p_change, code, date, type)
            cursor.execute(sql, param)
            conn.commit()
    
    cursor.close()
    conn.close()
    
    print 'p_change end: ', datetime.datetime.now()
    
# 计算当前收盘价与历史最高收盘价之比
def p2max(start = str(date.today()), end = str(date.today())):
    print 'p2max start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select code,type from stocks_info"
    
    cursor.execute(sql)
    codes_results = cursor.fetchall()
    
    for code_row in codes_results:
        code = code_row[0]
        type = code_row[1]
        
        sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
        param = (start, end)
        cursor.execute(sql, param)
        cal_results = cursor.fetchall()
        
        for cal_row in cal_results:
            date = cal_row[0]
            
            sql = "select close, max_price from k_data as k, stocks_summit as s where k.code = s.code and k.type = s.type and k.code=%s and k.date=%s and k.type=%s"
            param = (code, date, type)
            cursor.execute(sql, param)
            result = cursor.fetchone()
            
            if result:
                close = result[0]
                max_price = result[1]
                
                if max_price != 0:
                    p2max = round(float(close) / float(max_price), 2) * 100
                    
                    sql = "select id from stocks_extends where code=%s and date=%s and type=%s"
                    param = (code, date, type)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    
                    if exists:
                        sql = "update stocks_extends set p2max=%s where code=%s and date=%s and type=%s"
                    else:
                        sql = "insert into stocks_extends(p2max, code, date, type) values(%s, %s, %s, %s)"
                        
                    param = (p2max, code, date, type)
                    cursor.execute(sql, param)
                    conn.commit()
                    
    cursor.close()
    conn.close()
    
    print 'p2max end: ', datetime.datetime.now()
    
# 计算关注池收益率
def focus_pool_rate(today = str(date.today())):
    print 'focus_pool_rate start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate ='" + today + "'"
    cursor.execute(sql)
    dateRes = cursor.fetchone()
    
    if dateRes:
        # focus_pool_rate开始־
        now = time.time()
        sql = "insert into action_log(action_id, time) values(%s, %s)"
        param = (14, now)
        cursor.execute(sql, param)
        conn.commit()
        
        sql = "select code, cost_price, id, date from focus_pool where date < '" + today + "'"
        cursor.execute(sql)
        fpRes = cursor.fetchall()
        
        for fpRow in fpRes:
            code = fpRow[0]
            cost_price = fpRow[1]
            fp_id = fpRow[2]
            date = fpRow[3]
            
            sql = "select close from k_data where code=%s and date=%s"
            param = (code, today)
            cursor.execute(sql, param)
            k_data = cursor.fetchone()
            if k_data:
                yield_rate = (k_data[0] - cost_price) * 100.00 / cost_price
                sql = "update focus_pool set yield_rate=%s where id=%s"
                param = (yield_rate, fp_id)
                cursor.execute(sql, param)
                conn.commit()
                
                # 计算近3天收益率上升最快
                sql = "select close, date from k_data where code=%s order by date desc limit 3, 1"
                param = (code)
                cursor.execute(sql, param)
                rec3_row = cursor.fetchone()
                if rec3_row:
                    if rec3_row[1] > date:
                        rec3minus = (k_data[0] - rec3_row[0]) * 100.00 / cost_price
                    else:
                        rec3minus = 0.00
                # 计算近5天收益率上升最快
                sql = "select close, date from k_data where code=%s order by date desc limit 5, 1"
                param = (code)
                cursor.execute(sql, param)
                rec5_row = cursor.fetchone()
                if rec5_row:
                    if rec5_row[1] > date: 
                        rec5minus = (k_data[0] - rec5_row[0]) * 100.00 / cost_price
                    else:
                        rec5minus = 0.00
                # 更新rec3minus、rec5minus        
                sql = "update focus_pool set rec3minus=%s, rec5minus=%s where id=%s"
                param = (rec3minus, rec5minus, fp_id)
                cursor.execute(sql, param)
                conn.commit()
        
        # 统计最近3天收益率上升最快的top10
        sql = "select id, rec3topsdate from focus_pool where rec3minus > 0.00 order by rec3minus desc limit 10"
        cursor.execute(sql)
        rec3_res = cursor.fetchall()
        for rec3_row in rec3_res:
            rec3_id = rec3_row[0]
            rec3tops_date = rec3_row[1]
            
            if diff_between_two_days(today, rec3tops_date) > 30:
                sql = "update focus_pool set rec3tops=1, rec3topsdate=%s where id=%s"
            else:
                sql = "update focus_pool set rec3tops=rec3tops+1, rec3topsdate=%s where id=%s"
                
            param = (today, rec3_id)
            cursor.execute(sql, param)
            conn.commit()
            
        # 统计最近5天收益率上升最快的    
        sql = "select id, rec5topsdate from focus_pool where rec5minus > 0.00 order by rec5minus desc limit 10"
        cursor.execute(sql)
        rec5_res = cursor.fetchall()
        for rec5_row in rec5_res:
            rec5_id = rec5_row[0]
            rec5tops_date = rec5_row[1]
            
            if diff_between_two_days(today, rec5tops_date) > 30:
                sql = "update focus_pool set rec5tops=1, rec5topsdate=%s where id=%s"
            else:
                sql = "update focus_pool set rec5tops=rec5tops+1, rec5topsdate=%s where id=%s"
                
            param = (today, rec5_id)
            cursor.execute(sql, param)
            conn.commit()
                
        # focus_pool_rate结束־
        now = time.time()
        sql = "insert into action_log(action_id, time) values(%s, %s)"
        param = (15, now)
        cursor.execute(sql, param)
        conn.commit()
    
    cursor.close()
    conn.close()
    
    print 'focus_pool_rate end: ', datetime.datetime.now()
    
# 成交量相关计算（突破，缩量）
def volume(start = str(date.today()), end = str(date.today())):
    print 'volume start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    for row in results:
        date = row[0]
        
        sql = "select code, timeToMarket from stocks_info where type='S'"
        cursor.execute(sql)
        codes_results = cursor.fetchall()
        
        for code_row in codes_results:
            code = code_row[0]
            timeToMarket = code_row[1]
            
            if diff_between_two_days(date, timeToMarket) < 3*30:
                continue
            
            sql = "select volume from k_data where code=%s and date=%s and type='S'"
            param = (code, date)
            cursor.execute(sql, param)
            vol_result = cursor.fetchone()
            
            if vol_result:
                volume = vol_result[0]
            else:
                continue
            
            sql = "select v_ma5,v_ma10,v_ma20,v_ma60,v_ma120,max_vol5,max_vol10,max_vol20,max_vol60,max_vol120 from stocks_extends where code=%s and date=%s and type='S'"
            param = (code, date)
            cursor.execute(sql, param)
            extends_result = cursor.fetchone()
            
            if extends_result:
                v_ma5       = extends_result[0]
                v_ma10      = extends_result[1]
                v_ma20      = extends_result[2]
                v_ma60      = extends_result[3]
                v_ma120     = extends_result[4]
                max_vol5    = extends_result[5]
                max_vol10   = extends_result[6]
                max_vol20   = extends_result[7]
                max_vol60   = extends_result[8]
                max_vol120  = extends_result[9]
                
                v2ma5d = v2ma10d = v2ma20d = v2ma60d = v2ma120d = 0
                v2max = v2max5d = v2max10d = v2max20d = v2max60d = v2max120d = 0
                
                if v_ma5 != 0:
                    v2ma5d = round(volume / v_ma5, 2)
                if v_ma10 != 0:
                    v2ma10d = round(volume / v_ma10, 2)
                if v_ma20 != 0:
                    v2ma20d = round(volume / v_ma20, 2)
                if v_ma60 != 0:
                    v2ma60d = round(volume / v_ma60, 2)
                if v_ma120 != 0:
                    v2ma120d = round(volume / v_ma120, 2)
                if max_vol5 != 0:
                    v2max5d = round(volume / max_vol5, 2)
                if max_vol10 != 0:
                    v2max10d = round(volume / max_vol10, 2)
                if max_vol20 != 0:
                    v2max20d = round(volume / max_vol20, 2)
                if max_vol60 != 0:
                    v2max60d = round(volume / max_vol60, 2)
                if max_vol120 != 0:
                    v2max120d = round(volume / max_vol120, 2)
                    
                sql = "select id from volume where code=%s and date=%s"
                param = (code, date)
                cursor.execute(sql, param)
                exists = cursor.fetchone()
                
                if exists:
                    sql = '''update volume set v2ma5d=%s, v2ma10d=%s, v2ma20d=%s, v2ma60d=%s, v2ma120d=%s, v2max5d=%s, v2max10d=%s, v2max20d=%s, v2max60d=%s, v2max120d=%s where code=%s and date=%s'''
                else:
                    sql = '''insert into volume(v2ma5d, v2ma10d, v2ma20d, v2ma60d, v2ma120d, v2max5d, v2max10d, v2max20d, v2max60d, v2max120d, code, date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    
                param = (v2ma5d, v2ma10d, v2ma20d, v2ma60d, v2ma120d, v2max5d, v2max10d, v2max20d, v2max60d, v2max120d, code, date)
                cursor.execute(sql, param)
                conn.commit()
            
            sql = "select max_vol from stocks_summit where code=%s and type='S'"
            param = (code)
            cursor.execute(sql, param)
            max_vol_result = cursor.fetchone()
            
            if max_vol_result:
                max_vol = max_vol_result[0]
                
                if max_vol != 0:
                    v2max = round(volume / max_vol, 2)
                    
                    sql = "select id from volume where code=%s and date=%s"
                    param = (code, date)
                    cursor.execute(sql, param)
                    exists = cursor.fetchone()
                    
                    if exists:
                        sql = "update volume set v2max=%s where code=%s and date=%s"
                    else:
                        sql = "insert into volume(v2max, code, date) volues(%s, %s, %s)"
                        
                    param = (v2max, code, date)
                    cursor.execute(sql, param)
                    conn.commit()
                    
    cursor.close()
    conn.close()
    
    print 'volume end: ', datetime.datetime.now()
    
# 统计大单
def count_bigdeals(start = str(date.today()), end = str(date.today())):
    print 'count_bigdeals start: ', datetime.datetime.now()
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select code from stocks_info where type='S'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            
            df = ts.get_sina_dd(code, date, vol=200)
            if df is not None:
                dvalue = 0
                for index in df.index:
                    temp = df.ix[index]
                    if temp['type'] == '买盘':
                        dvalue += temp['volume'] * 100 * temp['price']
                    elif temp['type'] == '卖盘':
                        dvalue -= temp['volume'] * 100 * temp['price']
                
                sql = "insert into bigdeals(code, date, dvalue) values(%s, %s, %s)"
                param = (code, date, dvalue)
                cursor.execute(sql, param)
                conn.commit()
    
    cursor.close()
    conn.close()
    
    print 'count_bigdeals end: ', datetime.datetime.now()
    
# 实时统计大单
def count_bigdeals_realtime():
    print 'count_bigdeals_realtime start: ', datetime.datetime.now()

    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    today = str(date.today())
    morning_start = time.mktime(time.strptime(today + ' 09:25:00', '%Y-%m-%d %H:%M:%S'))
    morning_end = time.mktime(time.strptime(today + ' 11:30:00', '%Y-%m-%d %H:%M:%S'))
    afternoon_start = time.mktime(time.strptime(today + ' 13:00:00', '%Y-%m-%d %H:%M:%S'))
    afternoon_end = time.mktime(time.strptime(today + ' 15:00:00', '%Y-%m-%d %H:%M:%S'))
    while(True):
        now = time.time()
        nowstr = time.strftime('%H:%M', time.localtime(now))
        if now < morning_start or (now > morning_end and now < afternoon_start):
            continue
        if now > afternoon_end:
            break
        
        sql = "select code from stocks_info where type='S'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        top10_list = []
        for row in results:
            code = row[0]
            
            try:
                df = ts.get_sina_dd(code, today, vol=200)
                if df is not None:
                    dvalue = 0
                    for index in df.index:
                        temp = df.ix[index]
                        if temp['type'] == '买盘':
                            dvalue += temp['volume'] * 100 * temp['price']
                        elif temp['type'] == '卖盘':
                            dvalue -= temp['volume'] * 100 * temp['price']
                            
                    if len(top10_list) < 10:
                        top10_list.append((code, dvalue))
                    else:
                        top10_list = sorted(top10_list, key=lambda t:t[1], reverse = True)
                        if top10_list[9][1] < dvalue:
                            top10_list.pop()
                            top10_list.append((code, dvalue))  
            except:
                pass
        
        for item in top10_list:
            sql = "insert into `bigdeals_realtime`(`code`, `date`, `now`, `value`) values(%s, %s, %s, %s)"
            param = (item[0], today, nowstr, item[1])
            cursor.execute(sql, param)
            conn.commit()
        
    cursor.close()
    conn.close()
    
    print 'count_bigdeals_realtime end: ', datetime.datetime.now()
    
# 统计历史分笔的大额（50万元）数据
def count_tick_amount(start = str(date.today()), end = str(date.today())):
    print 'count_tick_amount start: ', datetime.datetime.now()
    
    # 单笔大额定义为50万
    big_amount = 500000
    
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
    cursor = conn.cursor()
    
    sql = "select calendarDate from trade_cal where calendarDate>=%s and calendarDate<=%s and isOpen=1"
    param = (start, end)
    cursor.execute(sql, param)
    cal_results = cursor.fetchall()
    
    for cal_row in cal_results:
        date = cal_row[0]
        
        sql = "select code from stocks_info where type='S'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            code = row[0]
            
            loop = True
            while(loop):
                try:
                    df = ts.get_tick_data(code, date, pause=3)
                    if df is not None:
                        amount_total = 0
                        for index in df.index:
                            temp = df.ix[index]
                            if temp['amount'] >= big_amount:
                                if temp['type'] == '买盘':
                                    amount_total += temp['amount']
                                elif temp['type'] == '卖盘':
                                    amount_total -= temp['amount']
                                    
                        sql = "insert into `tick_amount`(`code`, `date`, `amount`) values(%s, %s, %s)"
                        param = (code, date, amount_total)
                        cursor.execute(sql, param)
                        conn.commit()
                        
                    loop = False
                except:
                    print code
    
    cursor.close()
    conn.close()
    
    print 'count_tick_amount end: ', datetime.datetime.now()
    