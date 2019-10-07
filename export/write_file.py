#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/15 5:03 PM
@Author  : red
@Site    : 
@File    : write_file.py
@Software: PyCharm
"""
import sys
sys.path.append('../utils')
import time
import threading
import os
import file_util, dir_util
# from export import export_data_txt_one
import export_data_txt_one


class Thread(threading.Thread):
    def __init__(self, num, lst, path):
        self._path = path
        self._num = num
        self._lst = lst
        super().__init__()

    def run(self):
        print("[{}]--write file start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._num, len(self._lst)))

        for element in self._lst:
            file_util.write_file(os.path.join(self._path, element[0] + '.txt'),
                                 element[1])
        print("[{}]--write file end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start(path, data, step=1000):
    temp_list = [data[i:i + step] for i in range(0, len(data), step)]
    thr_list = [Thread(i, temp_list[i], path) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


def start_main(limit):
    path = "/root/data/news/500data"
    # 清空文件夹
    dir_util.remove_dir("/root/data/news/500data")
    # 创建文件夹
    dir_util.mkdir([os.path.join(path, 'sina'), os.path.join(path, 'sohu'), os.path.join(path, 'tianya')])
    # 获取数据
    sina, sohu, tianya = export_data_txt_one.main(limit)
    start(str(os.path.join(path, 'sina')), sina, 5000)
    start(str(os.path.join(path, 'sohu')), sohu, 5000)
    start(str(os.path.join(path, 'tianya')), tianya, 5000)
