# -*- coding: utf-8 -*-
from super_wave import *
from model import *
from statistics import *

today = str(date.today())
start = today
end = today

# start = '2017-08-14'  
# today = '2017-08-14'
# end = today

super_wave(today)
super_wave_init(today)

ene(start, end)
handle_close_ene_lower(start, end)

handle_max_ma_vol(start, end)
handle_ma(start, end)

volume(start, end)
volume_break(start, end)

p_change(start, end)
p2max(start, end)

focus_pool_rate(today)

# 统计大单
count_bigdeals(today, today)