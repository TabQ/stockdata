# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys

print datetime.datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

# std_info入库开始记入日志
now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (3, now)
cursor.execute(sql, param)
conn.commit()

sql = "select code from stocks_info"

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
	code = row[0]

	# get max volume and min price
	df = ts.get_hist_data(code)
	if df is None:
		continue

	max_vol = 0
	maxvol_date = ''
	min_price = 1000
	min_date = ''
	for date in df.index:
		if df.ix[date]['volume'] > max_vol:
			max_vol = df.ix[date]['volume']
			maxvol_date = date
		if df.ix[date]['low'] < min_price:
			min_price = df.ix[date]['low']
			min_date = date
			
	sql = "update stocks_info set maxVol=%s, maxVolDate=%s, minPrice=%s, minPriceDate=%s where code='" + code + "'"
	param = (max_vol, maxvol_date, min_price, min_date)
	cursor.execute(sql, param)
	conn.commit()
	
# std_info入库结束记入日志
now = time.time()
sql = "insert into action_log(action_id, time) values(%s, %s)"
param = (4, now)
cursor.execute(sql, param)
conn.commit()

cursor.close()
conn.close()

print datetime.datetime.now()