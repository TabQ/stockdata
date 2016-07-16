import tushare as ts
import MySQLdb
import time,datetime
from datetime import date

today = str(date.today())

start_time_str = today + ' 09:30:00'
start_time_str_tmp = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
start_time_unix = time.mktime(start_time_str_tmp.timetuple())

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="stock", charset="utf8")
cursor = conn.cursor()

sql = "select code, v_ma20 from std_info"

cursor.execute(sql)
results = cursor.fetchall()

i = 0
while True:
    process_time_unix = time.time()
    if process_time_unix > start_time_unix + 14400:
        break
    
    i += 1
    print '----------------- ' + str(i) + ' -----------------'
    print datetime.datetime.now()
    
    for row in results:
        code = row[0]
        v_ma20 = row[1]
        
        if v_ma20 == 0:
            continue
        
        try:
            df = ts.get_realtime_quotes(code)
            if df is None:
                continue
            
            volume = int(df.ix[0]['volume']) / 100
                
            now_time_str = df.ix[0]['date'] + ' ' + df.ix[0]['time']
            now_time_str_tmp = datetime.datetime.strptime(now_time_str, "%Y-%m-%d %H:%M:%S")
            now_time_unix = time.mktime(now_time_str_tmp.timetuple())
            
            hope_vol = volume * 14400 / (now_time_unix - start_time_unix)
            
            if hope_vol > 4 * v_ma20:
                hopevol_2_ma20 = hope_vol / v_ma20
                print '| ' + df.ix[0]['code'], str(hopevol_2_ma20) + ' | ',
                sql = "insert into alarm(code, hopevol_2_ma20, alert_time, v_ma20, date) values(%s, %s, %s, %s, %s)"
                param = (code, hopevol_2_ma20, now_time_str, v_ma20, today)
                cursor.execute(sql, param)
                conn.commit()
        except Exception,e:
            print
            print Exception,":",e
            
    print datetime.datetime.now()
    
cursor.close()
conn.close()