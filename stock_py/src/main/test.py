# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import sys
from common import *
from statistics import p_change

# from main import model
# from model import volume_break
# 
# conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
# cursor = conn.cursor()
# 
# for i in range(369, 393):
#     sql = "select calendarDate from trade_cal where id="+str(i)
#     cursor.execute(sql)
#     result = cursor.fetchone()
#     
#     today = result[0]
#     volume_break(today)
#     model(today)
#         
# cursor.close()
# conn.close()

p_change('2017-02-07', '2017-02-07')