#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/23 7:19 PM
@Author  : red
@Site    : 
@File    : rename_file.py
@Software: PyCharm
"""
import time
import os
from utils import file_util as file

path_len = 8
path = "/Users/red/Desktop/temp/news/data/500data"
path_list = [os.path.join(path, 'sina'), os.path.join(path, 'sohu'), os.path.join(path, 'tianya')]


def rename_file():
    print("[{}]--start process rename file......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    result = []
    for element in path_list:
        result.append(file.get_file_list(element, []))

    for element in result:
        count = 0
        for item in element:
            (filepath, tempfilename) = os.path.split(item)
            os.rename(item, os.path.join(filepath, '0' * (path_len - len(str(count))) + str(count) + '.txt'))
            count += 1
    print("[{}]--end process rename file......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start():
    rename_file()
