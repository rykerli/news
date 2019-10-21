#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/10/21 6:14 PM
@Author  : red
@Site    : 
@File    : extract_origin_data.py
@Software: PyCharm
"""
import time
import sys

sys.path.append('../utils')
import time
import sql_util as sql
import file_util
from operator import itemgetter
from itertools import groupby
import re
import time
import threading


def get_sina_data(limit, min_num, max_num):
    print("[{}]--start process sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sina_article = sql.queryall(
            "select * from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + min_num
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + max_num + " limit " + str(
                limit))
    else:
        sina_article = sql.queryall(
            "select * from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + min_num
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + max_num + "")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def get_tianya_data(limit, min_num, max_num):
    print("[{}]--start process tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        ty_article = sql.queryall(
            "select * from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + min_num
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + max_num + " limit " + str(limit))
    else:
        ty_article = sql.queryall(
            "select * from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + min_num
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + max_num + "")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def get_sohu_data(limit, min_num, max_num):
    print("[{}]--start process sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sohu_article = sql.queryall(
            "select * from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + min_num
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + max_num + " limit " + str(limit))
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_origin_data where CHAR_LENGTH(TRIM(content)) > " + min_num
            + " and CHAR_LENGTH(TRIM(content)) < " + max_num + " limit " + str(limit))
    else:
        sohu_article = sql.queryall(
            "select * from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + min_num
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + max_num + "")
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_origin_data where CHAR_LENGTH(TRIM(content)) > " + min_num
            + " and CHAR_LENGTH(TRIM(content)) < " + max_num + "")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_article, bzy_sohu_article


def process_sina_data(limit, min_num, max_num):
    print("[{}]--start process data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = get_sina_data(limit, min_num, max_num)
    # sina_result = []
    #
    # for element in sina_article:
    #     temp = [str(element.get('id')), str(element.get('post_content_txt'))]
    #     sina_result.append(temp)
    print("[{}]--process data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def process_tianya_data(limit, min_num, max_num):
    print("[{}]--start process tianya data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    ty_article = get_tianya_data(limit, min_num, max_num)
    # ty_result = []
    # for element in ty_article:
    #     temp = [str(element.get('id')), str(element.get('question_detail'))]
    #     ty_result.append(temp)

    print("[{}]--process tianya data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def process_sohu_data(limit, min_num, max_num):
    print("[{}]--start process sohu data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_article, bzy_sohu_article = get_sohu_data(limit, min_num, max_num)
    start(sohu_article)
    print(sj_sohu_result)
    print("[{}]--process sj sohu data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    # return null


sj_sohu_result = []


class Thread(threading.Thread):
    def __init__(self, num, lst):
        self._num = num
        self._lst = lst
        super().__init__()

    def run(self):
        print("[{}]--process start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._num, len(self._lst)))
        # 循环处理数据，去掉每一条数据中的article_content html标签
        # 正则表达式过滤标签<>...</> or <.../>
        # for element in self._lst:
        #     file_util.write_file(os.path.join(self._path, element[0] + '.txt'),
        #                          element[1])
        count = 0
        for element in self._lst:
            temp = re.compile(r'<[^>]*>', re.S)
            temp = temp.sub('', element.get('article_content'))
            temp = str.replace(temp, '\n', '').strip()
            element.set('article_content', temp)
            sj_sohu_result.append(element)
            count += 1
        print("[{}]--process end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start(sohu_article, step=5000):
    temp_list = [sohu_article[i:i + step] for i in range(0, len(sohu_article), step)]
    thr_list = [Thread(i, temp_list[i]) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


def main(limit, min_num, max_num):
    return process_sina_data(limit, min_num, max_num), process_sohu_data(limit, min_num, max_num), process_tianya_data(
        limit, min_num, max_num)


if __name__ == '__main__':
    process_sohu_data(2000, 80, 1800)
