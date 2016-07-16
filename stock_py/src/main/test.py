# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "update focus_pool set yield_rate=0"
cursor.execute(sql)
conn.commit()

cursor.close()
conn.close()