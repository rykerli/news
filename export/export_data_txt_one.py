#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/15 4:14 PM
@Author  : red
@Site    : 
@File    : export_data_txt_one.py
@Software: PyCharm

"""
import sys
sys.path.append('../utils')
import time
import sql_util as sql
import file_util
from operator import itemgetter
from itertools import groupby


def get_sina_data(limit):
    print("[{}]--start process sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sina_article = sql.queryall(
            "select * from sj_sina_article where CHAR_LENGTH(post_content_txt) > 50 limit " + str(limit))
    else:
        sina_article = sql.queryall(
            "select * from sj_sina_article")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def get_tianya_data(limit):
    print("[{}]--start process tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        ty_article = sql.queryall(
            "select * from sj_tianya_article where CHAR_LENGTH(question_detail) > 50 limit " + str(limit))
    else:
        ty_article = sql.queryall(
            "select * from sj_tianya_article")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def get_sohu_data(limit):
    print("[{}]--start process sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sohu_article = sql.queryall("select * from sj_sohu_no_html where CHAR_LENGTH(article_content) > 50 limit " + str(limit))
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_article where CHAR_LENGTH(content) >50 limit " + str(limit))
    else:
        sohu_article = sql.queryall("select * from sj_sohu_no_html")
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_article")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_article, bzy_sohu_article


def process_sina_data(limit):
    print("[{}]--start process data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = get_sina_data(limit)
    sina_result = []

    for element in sina_article:
        temp = [str(element.get('id')), str(element.get('post_content_txt'))]
        sina_result.append(temp)
    print("[{}]--process data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_result


def process_tianya_data(limit):
    print("[{}]--start process tianya data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    ty_article = get_tianya_data(limit)
    ty_result = []
    for element in ty_article:
        temp = [str(element.get('id')), str(element.get('question_detail'))]
        ty_result.append(temp)

    print("[{}]--process tianya data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_result


def process_sohu_data(limit):
    print("[{}]--start process sohu data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_article, bzy_sohu_article = get_sohu_data(limit)
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


def main(limit):
    return process_sina_data(limit), process_sohu_data(limit), process_tianya_data(limit)