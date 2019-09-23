#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/15 5:25 PM
@Author  : red
@Site    : 
@File    : dir_util.py
@Software: PyCharm
"""
import time
import shutil
import os


def remove_dir(file_path):
    if os.path.exists(file_path):
        print("[{}]--start process remove dir......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        shutil.rmtree(file_path)
        os.mkdir(file_path)
        print("[{}]--end process remove dir......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    else:
        os.mkdir(file_path)


def mkdir(item):
    print("[{}]--start process mkdir......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if isinstance(item, str):
        os.mkdir(item)
    elif isinstance(item, list):
        for element in item:
            os.mkdir(element)
    else:
        raise SystemExit('Parameter error!')
    print("[{}]--end process mkdir......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
