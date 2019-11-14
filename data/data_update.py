#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/11/14 4:48 PM
@Author  : red
@Site    : 
@File    : data_update.py
@Software: PyCharm
"""
import time
from utils import sql_util as sql
from utils import xlwt_util
from utils import excel_util


def read_data(path):
    file_list = excel_util.get_file_list(path, [])

    for element in file_list:
        print(element)


if __name__ == '__main__':
    read_data("/Users/red/Desktop/temp/news/会议记录/20191113语料筛选")
