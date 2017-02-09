# -*- coding: utf-8 -*-
import MySQLdb
import datetime
from datetime import date
import time

# 计算两个日期间间隔的天数
def diff_between_two_days(day1, day2):
    if day1 == '0' or day2 == '0':
        return 0
    if day1 == '' or day2 == '':
        return 0
    
    if '-' not in day1:
        day1 = day1[:4] + '-' + day1[4:6] + '-' + day1[6:]
    if '-' not in day2:
        day2 = day2[:4] + '-' + day2[4:6] + '-' + day2[6:]
    
    second1 = datetime.datetime.strptime(day1, "%Y-%m-%d")
    second1 = time.mktime(second1.timetuple())
    
    second2 = datetime.datetime.strptime(day2, "%Y-%m-%d")
    second2 = time.mktime(second2.timetuple())
    
    if(second1 < second2):
        tmp = second2
        second2 = second1
        second1 = tmp
        
    return (second1 - second2) / 86400

# 计算某支股票某日的某条移动平均线
def ma_date(cursor, code, type = 'S', date = str(date.today()), n = 5):
    code = get_code(code, type)
    
    sql = "select close from k_data where code=%s and type=%s and date<=%s order by date desc limit %s"
    param = (code, type, date, n)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    count = 0
    sum = 0
    
    for row in results:
        sum += row[0]
        count += 1
        
    if count == n:
        sum /= n
        sum = round(sum, 2)
    else:
        sum = -1
        
    return sum
    
# 计算某支股票某日的某条均量
def ma_vol_date(cursor, code, type='S', date = str(date.today()), n = 5):
    code = get_code(code, type)
    
    sql = "select volume from k_data where code=%s and type=%s and date<=%s order by date desc limit %s"
    param = (code, type, date, n)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    count = 0
    sum = 0
    
    for row in results:
        sum += row[0]
        count += 1
        
    if count == n:
        sum /= n
        sum = round(sum, 0)
    else:
        sum = -1
        
    return sum

# 计算某支股票n日的最大成交量以及某日的某条均量n
def max_ma_vol_date(cursor, code, type = 'S', date = str(date.today()), n = 5):
    code = get_code(code, type)
    
    sql = "select volume from k_data where code=%s and type=%s and date<=%s order by date desc limit %s"
    param = (code, type, date, n)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    count = 0
    sum = 0
    max = 0
    
    for row in results:
        sum += row[0]
        count += 1
        
        if row[0] > max:
            max = row[0]
            
    if count == n:
        sum /= n
        sum = round(sum, 0)
        
        result = (max, sum)
    else:
        result = -1
        
    return result

# 计算某支股票的最大成交量
def max_vol(cursor, code, type='S'):
    code = get_code(code, type)
    
    sql = "select volume from k_data where code=%s and type=%s"
    param = (code, type)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    max = 0
    for row in results:
        if row[0] > max:
            max = row[0]
            
    return max

# 计算某支股票的最高收盘价
def max_price(cursor, code, type='S'):
    code = get_code(code, type)
    
    sql = "select close from k_data where code=%s and type=%s"
    param = (code, type)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    max = 0
    for row in results:
        if row[0] > max:
            max = row[0]
            
    return max

# 同时计算某支股票的最大成交量及最高收盘价
def max_vol_price(cursor, code, type='S'):
    code = get_code(code, type)
    
    sql = "select volume, close from k_data where code=%s and type=%s"
    param = (code, type)
    cursor.execute(sql, param)
    results = cursor.fetchall()
    
    max_vol = 0
    max_price = 0
    for row in results:
        if row[0] > max_vol:
            max_vol = row[0]
        if row[1] > max_price:
            max_price = row[1]
            
    return (max_vol, max_price)

# 统一获取code
def get_code(code, type='S'):
    if type == 'S':
        result = code
    elif code == '000001':
        result = 'sh' + code
    else:
        result = 'sz' + code
        
    return result