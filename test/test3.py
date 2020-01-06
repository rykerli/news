#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2020/1/6 11:23 AM
@Author  : red
@Site    : 
@File    : test3.py
@Software: PyCharm
"""
import time
import sys

sys.path.append('../utils')
import sql_util as sql

if __name__ == '__main__':
    result = sql.queryall('select * from sina where number = %s', '00000001')
    if not result:
        print('none')
    print(type(result))
    print(result)
