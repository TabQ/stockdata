import tushare as ts
from datetime import date

today = str(date.today())

df = ts.top_list(today)

print df