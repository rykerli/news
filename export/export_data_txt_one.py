#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/15 4:14 PM
@Author  : red
@Site    : 
@File    : export_data_txt_one.py
@Software: PyCharm
"""
import time
from utils import sql_util as sql
from utils import file_util
from operator import itemgetter
from itertools import groupby


def get_sina_data(count):
    print("[{}]--start process sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = sql.queryall(
        "select * from sj_sina_article where CHAR_LENGTH(post_content_txt) > 20 limit " + str(count))

    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def get_tianya_data(count):
    print("[{}]--start process tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    ty_article = sql.queryall(
        "select * from sj_tianya_article where CHAR_LENGTH(question_detail) > 20 limit " + str(count))
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def get_sohu_data(count):
    print("[{}]--start process sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    sohu_article = sql.queryall("select * from sj_sohu where CHAR_LENGTH(article_content) > 20 limit " + str(count))
    bzy_sohu_article = sql.queryall(
        "select * from bzy_sohu_article where CHAR_LENGTH(content) > 20 limit " + str(count))

    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_article, bzy_sohu_article


def process_sina_data(count):
    print("[{}]--start process data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = get_sina_data(count)
    sina_result = []

    for element in sina_article:
        temp = [str(element.get('id')), str(element.get('post_content_txt'))]
        sina_result.append(temp)
    print("[{}]--process data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_result


def process_tianya_data(count):
    print("[{}]--start process tianya data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    ty_article = get_tianya_data(count)
    ty_result = []
    for element in ty_article:
        temp = [str(element.get('id')), str(element.get('question_detail'))]
        ty_result.append(temp)

    print("[{}]--process tianya data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_result


def process_sohu_data(count):
    print("[{}]--start process sohu data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_article, bzy_sohu_article = get_sohu_data(count)
    sohu_result = []

    for element in bzy_sohu_article:
        temp = [element.get('id'), element.get('content')]
        sohu_result.append(temp)
    print("[{}]--process bzy sohu data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    for element in sohu_article:
        temp = [element.get('id'), element.get('article_content')]
        sohu_result.append(temp)
    print("[{}]--process sj sohu data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_result


def main():
    return process_sina_data(500), process_sohu_data(250), process_tianya_data(500)


if __name__ == '__main__':
    file_path = '/Users/red/Desktop/temp/news/data/all_data.txt'

    # sina = process_sina_data()
    # print(sina)
    # bzy和sj各250篇
    sohu = process_sohu_data(250)
    print(sohu)
    # tianya = process_tianya_data(500)
    # print(tianya)

    # file_util.append_file(file_path, str(sina))
