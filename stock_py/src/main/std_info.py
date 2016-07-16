import tushare as ts
import MySQLdb
from datetime import date
import datetime

print datetime.datetime.now()

today = str(date.today())

# today = '2016-06-24'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select code from stocks_info"

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    code = row[0]
    
    # get max volume
    df = ts.get_hist_data(code)
    if df is None:
        continue
    
    max_vol = 0
    maxvol_date = ''
    v_ma20 = 0
    for date in df.index:
        if df.ix[date]['volume'] > max_vol:
            max_vol = df.ix[date]['volume']
            maxvol_date = date
          
        # get v_ma20    
        if date == today:
            v_ma20 = df.ix[date]['v_ma20']
    
    if v_ma20 != 0:
        sql = "replace into std_info values(%s, %s, %s, %s, %s)"
        param = (code, max_vol, maxvol_date, v_ma20, today)
        cursor.execute(sql, param)
        conn.commit()
        
cursor.close()
conn.close()

print datetime.datetime.now()