#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-06-23 11:03
@Author  : red
@Site    : 
@File    : export_data_to_txt.py
@Software: PyCharm
"""
import time
from utils import sql_util as sql
from utils import file_util
from operator import itemgetter
from itertools import groupby


def get_sina_data():
    print("[{}]--start process sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = sql.queryall("select * from sj_sina_article")
    sina_comment = sql.queryall("select * from sj_sina_comment")

    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article, sina_comment


def get_tianya_data():
    print("[{}]--start process tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    ty_article = sql.queryall("select * from sj_tianya_article")
    ty_comment = sql.queryall("select * from sj_tianya_comment")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article, ty_comment


def get_sohu_data():
    print("[{}]--start process sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    sohu_article = sql.queryall("select * from sj_sohu")
    bzy_sohu_article = sql.queryall("select * from bzy_sohu_article")
    bzy_sohu_comment = sql.queryall("select * from bzy_sohu_comment")

    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_article, bzy_sohu_article, bzy_sohu_comment


def process_sina_data():
    print("[{}]--start process data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article, sina_comment = get_sina_data()
    sina_result = []

    # 处理sina数据
    sina_comment.sort(key=itemgetter('article_id'))
    for article_id, items in groupby(sina_comment, key=itemgetter('article_id')):
        temp = []
        [temp.append(element.get('post_content_txt')) for element in sina_article if element.get('id') == article_id]
        [temp.append(i.get('comment_content')) for i in items]
        sina_result.append(temp)
    print("[{}]--process data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_result


def process_tianya_data():
    print("[{}]--start process tianya data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    ty_article, ty_comment = get_tianya_data()
    ty_result = []

    # 处理tianya数据
    ty_comment.sort(key=itemgetter('article_id'))
    for article_id, items in groupby(ty_comment, key=itemgetter('article_id')):
        temp = []
        [temp.append(element.get('question_detail')) for element in ty_article if element.get('id') == article_id]
        [temp.append(i.get('question_answer_content')) for i in items]
        ty_result.append(temp)
    print("[{}]--process tianya data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_result


def process_sohu_data():
    print("[{}]--start process sohu data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_article, bzy_sohu_article, bzy_sohu_comment = get_sohu_data()
    sohu_result = []

    # 处理tianya数据
    bzy_sohu_comment.sort(key=itemgetter('article_id'))
    for article_id, items in groupby(bzy_sohu_comment, key=itemgetter('article_id')):
        temp = []
        [temp.append(element.get('content')) for element in bzy_sohu_article if element.get('id') == article_id]
        [temp.append(i.get('comment')) for i in items]
        sohu_result.append(temp)
    print("[{}]--process sohu data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    for element in sohu_article:
        sohu_result.append(element.get('article_content'))
    return sohu_result


if __name__ == '__main__':
    file_path = '/Users/red/Desktop/temp/news/data/all_data.txt'

    sina = process_sina_data()
    # sohu = process_sohu_data()
    # tianya = process_tianya_data()
    # print(sohu)
    # print(tianya)

    file_util.append_file(file_path, str(sina))
