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

df = ts.get_concept_classified()
for id in df.index:
    sql = "insert into stocks_concept(code, name, concept) values(%s,%s,%s)"
    param = (df.ix[id]['code'], df.ix[id]['name'], df.ix[id]['c_name'])
    cursor.execute(sql, param)
    conn.commit()
    
cursor.close()
conn.close()

print datetime.datetime.now()