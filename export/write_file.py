#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/15 5:03 PM
@Author  : red
@Site    : 
@File    : write_file.py
@Software: PyCharm
"""
import time
import threading
import os
from utils import file_util, dir_util
from export import export_data_txt_one


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


def start(path, data, step=100):
    temp_list = [data[i:i + step] for i in range(0, len(data), step)]
    thr_list = [Thread(i, temp_list[i], path) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


if __name__ == '__main__':
    path = "/Users/red/Desktop/temp/news/data/500data"
    # 清空文件夹
    dir_util.remove_dir("/Users/red/Desktop/temp/news/data/500data")
    # 创建文件夹
    dir_util.mkdir([os.path.join(path, 'sina'), os.path.join(path, 'sohu'), os.path.join(path, 'tianya')])
    # 获取数据
    sina, sohu, tianya = export_data_txt_one.main()
    start(str(os.path.join(path, 'sina')), sina, 100)
    start(str(os.path.join(path, 'sohu')), sohu, 100)
    start(str(os.path.join(path, 'tianya')), tianya, 100)
