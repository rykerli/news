#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-01-07 08:57
@Author  : red
@Site    : 
@File    : seg_word.py
@Software: PyCharm
"""
import jieba_fast as jieba
import configparser as cf
import codecs
import uuid
import time
import threading
from utils import sql_util

# 开启并行分词模式，参数为并行进程数
jieba.enable_parallel(4)


def get_file_path(section, key):
    conf = cf.ConfigParser()
    conf.read('../conf/config.cfg')
    return conf.get(section, key)


def get_stop_word():
    with codecs.open(get_file_path('stop_file', 'stop_words_chinese_1'), 'r', encoding='utf8') as f1:
        data1 = f1.read()

    with codecs.open(get_file_path('stop_file', 'stop_words_english_1'), 'r') as f2:
        data2 = f2.read()
    f_stop_list = (data1 + data2).split('\n')
    return f_stop_list


def write_file(file_path, content):
    with codecs.open(file_path, 'w', encoding='utf8') as w:
        w.write(u" ".join(content))


def split(stop_lists, data):
    word_list = []
    seg_list = jieba.cut(data, cut_all=False)
    list_str = " ".join(seg_list)

    for word in list_str.split(" "):
        if not (word.strip().lower() in stop_lists) and len(word.strip()) > 1:
            word_list.append(word)
    write_file("/Users/red/Desktop/temp/news/data/word/" + str(uuid.uuid4()) + ".txt", word_list)


class MyThread(threading.Thread):
    def __init__(self, num, data_list):
        self._num = num
        self._data_list = data_list
        super().__init__()

    def run(self):
        start_writer_file = time.time()
        count = 0
        for content in self._data_list:
            count += 1
            split(stop_word_list, content)
            if count % 100 == 0:
                print("processed %d records" % count)
        print("process the %d thread, records total num is %d" % (self._num, count))
        end_writer_file = time.time() - start_writer_file
        print("split the {:.0f} thread, records  time  {:.0f}m {:.0f}s".format(self._num,
                                                                               end_writer_file // 60,
                                                                               end_writer_file % 60))


if __name__ == '__main__':
    stop_word_list = get_stop_word()

    num = sql_util.queryone("select count(*) from origin_data")

    limit = 1000
    count = 0
    for temp in range(0, num, limit):
        data = sql_util.queryall("select content from origin_data limit %s,%s", (temp, count + limit))
        count += limit
        step = 100

        temp_list = [data[i:i + step] for i in range(0, len(data), step)]
        thr_list = [MyThread(i, temp_list[i]) for i in range(len(temp_list))]
        [thr.start() for thr in thr_list]
        [thr.join() for thr in thr_list]
