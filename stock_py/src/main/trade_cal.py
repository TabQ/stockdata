import tushare as ts
import MySQLdb
from datetime import date
import datetime

print datetime.datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

ts.set_token('e8596c92be7248552f8fa6b4af32f5c8eed01e2044b0962313fdaec5e69e5d5c')
mt = ts.Master()
df = mt.TradeCal(exchangeCD='XSHG', beginDate='20180101', endDate='20181231', field='exchangeCD,calendarDate,isOpen,prevTradeDate,isWeekEnd,isMonthEnd,isQuarterEnd,isYearEnd')

if df is not None:
    for idx in df.index:
        temp = df.ix[idx]
        sql = "insert into trade_cal(exchangeCD,calendarDate,isOpen,prevTradeDate,isWeekEnd,isMonthEnd,isQuarterEnd,isYearEnd) \
        values(%s,%s,%s,%s,%s,%s,%s,%s)"
        param = (temp['exchangeCD'],temp['calendarDate'],temp['isOpen'],temp['prevTradeDate'],temp['isWeekEnd'],temp['isMonthEnd'],temp['isQuarterEnd'],temp['isYearEnd'])
        cursor.execute(sql, param)
        conn.commit()
        
cursor.close()
conn.close()

print datetime.datetime.now()