# -*- coding: utf-8 -*-
import tushare as ts
import sys

df = ts.get_today_all()
for index in df.index:
    temp = df.ix[index]
#     if temp['code'] == '002817':
    print temp['name'],temp['nmc']