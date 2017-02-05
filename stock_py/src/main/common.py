# -*- coding: utf-8 -*-
import datetime
import time

def diff_between_two_days(day1, day2):
    if day1 == '0' or day2 == '0':
        return 0
    if day1 == '' or day2 == '':
        return 0
    
    second1 = datetime.datetime.strptime(day1, "%Y-%m-%d")
    second1 = time.mktime(second1.timetuple())
    
    second2 = datetime.datetime.strptime(day2, "%Y%m%d")
    second2 = time.mktime(second2.timetuple())
    
    if(second1 < second2):
        tmp = second2
        second2 = second1
        second1 = tmp
        
    return (second1 - second2) / 86400