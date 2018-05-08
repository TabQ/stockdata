# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
from model import second_limitup
from statistics import count_bigdeals, count_bigdeals_realtime, count_tick_amount

# today = str(date.today())
today = '2017-08-16'

# second_limitup('2017-02-01', '2017-02-28')
# count_bigdeals_realtime()
# count_bigdeals(today, today)

# df = ts.get_sina_dd('600516', '2017-08-16', 200)
# count = 0
# for index in df.index:
#     temp = df.ix[index]
#     print temp


count_tick_amount(today, today)