# -*- coding: utf-8 -*-
import tushare as ts
import MySQLdb
from datetime import date
import datetime
import time
import traceback
import os

print datetime.datetime.now()

today = str(date.today())

today = '2016-07-01'

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select calendarDate from trade_cal where isOpen=1 and calendarDate='" + today + "'"
cursor.execute(sql)
dateRes = cursor.fetchone()

if dateRes:
    # 每日龙虎榜列表
    try:
        df = ts.top_list(today)
        if df is not None:
            for idx in df.index:
                temp = df.ix[idx]
                sql = "insert into top_list(code,name,pchange,amount,buy,bratio,sell,sratio,reason,date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (temp['code'],temp['name'],temp['pchange'],temp['amount'],temp['buy'],temp['bratio'],temp['sell'],temp['sratio'],temp['reason'],temp['date'])
                cursor.execute(sql, param)
                conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        
    # 个股上榜统计            
    try:
        df = idx = temp = sql = param = None
        df = ts.cap_tops()
        if df is not None:
            for idx in df.index:
                temp = df.ix[idx]
                sql = "insert into cap_tops(code,name,count,bamount,samount,net,bcount,scount) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (temp['code'],temp['name'],temp['count'],temp['bamount'],temp['samount'],temp['net'],temp['bcount'],temp['scount'])
                cursor.execute(sql, param)
                conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        
    # 营业部上榜统计    
    try:                
        df = idx = temp = sql = param = None
        df = ts.broker_tops()
        if df is not None:
            for idx in df.index:
                temp = df.ix[idx]
                sql = "insert into broker_tops(broker,count,bamount,bcount,samount,scount,top3) values(%s,%s,%s,%s,%s,%s,%s)"
                param = (temp['broker'],temp['count'],temp['bamount'],temp['bcount'],temp['samount'],temp['scount'],temp['top3'])
                cursor.execute(sql, param)
                conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
    
    # 机构席位追踪    
    try:                
        df = idx = temp = sql = param = None
        df = ts.inst_tops()
        if df is not None:
            for idx in df.index:
                temp = df.ix[idx]
                sql = "insert into inst_tops(code,name,bamount,bcount,samount,scount,net) values(%s,%s,%s,%s,%s,%s,%s)"
                param = (temp['code'],temp['name'],temp['bamount'],temp['bcount'],temp['samount'],temp['scount'],temp['net'])
                cursor.execute(sql,param)
                conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        
    # 机构成交明细
    try:
        df = idx = temp = sql = param = None
        df = ts.inst_detail()
        if df is not None:
            for idx in df.index:
                temp = df.ix[idx]
                sql = "insert into inst_detail(code,name,date,bamount,samount,type) values(%s,%s,%s,%s,%s,%s)"
                param = (temp['code'],temp['name'],temp['date'],temp['bamount'],temp['samount'],temp['type'])
                cursor.execute(sql,param)
                conn.commit()
    except:
        f=open("errors/"+today+".log",'a')
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        
cursor.close()
conn.close()

print datetime.datetime.now()