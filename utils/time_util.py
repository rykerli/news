#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2018-12-21 17:41
@Author  : red
@Site    : 
@File    : time_util.py
@Software: PyCharm

"""
import time
import datetime


def stamp_to_date(stamp):
    # 时间戳转日期
    #     ts = '1553858160'
    dt1 = datetime.datetime.fromtimestamp(float(stamp)/10**(len(stamp)-10))
    return dt1


def date_to_stamp(time_str):
    # 日期转时间戳
    #time_str = '2019-03-29 19:16'
    #转换成时间数组
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M")
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)