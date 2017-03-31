# -*- coding: utf-8 -*-
from __future__ import division

# 移动平均线（ma）计算公式
def ma(x):
    result = 0
    
    for value in x:
        result += value
        
    return result / len(x)    

# 指数平均数指标（ema）计算公式
def ema(x):
    return x[0] if len(x) == 1 else (2 * x[len(x)-1] + (len(x)-1) * ema(x[0:len(x)-1])) / (len(x) + 1)