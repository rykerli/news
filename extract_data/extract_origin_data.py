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
import sql_util as sql
# import file_util
# from operator import itemgetter
# from itertools import groupby
import re
import time_util
import threading

path_len = 8


def get_sina_data(limit, min_num, max_num):
    print("[{}]--start process sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sina_article = sql.queryall(
            "select * from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + str(max_num) + " limit " + str(
                limit))
    else:
        sina_article = sql.queryall(
            "select * from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + str(max_num) + "")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def get_tianya_data(limit, min_num, max_num):
    print("[{}]--start process tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        ty_article = sql.queryall(
            "select * from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + str(max_num) + " limit " + str(limit))
    else:
        ty_article = sql.queryall(
            "select * from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + str(max_num) + "")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def get_sohu_data(limit, min_num, max_num):
    print("[{}]--start process sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sohu_article = sql.queryall(
            "select * from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + str(min_num)
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + str(max_num) + " limit " + str(limit))
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_article where CHAR_LENGTH(TRIM(content)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(content)) < " + str(max_num) + " limit " + str(limit))
    else:
        sohu_article = sql.queryall(
            "select * from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + str(min_num)
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + str(max_num) + "")
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_article where CHAR_LENGTH(TRIM(content)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(content)) < " + str(max_num) + "")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_article, bzy_sohu_article


def process_sina_data(limit, min_num, max_num):
    print("[{}]--start process data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = get_sina_data(limit, min_num, max_num)
    count = 0
    for item in sina_article:
        item['word_count'] = len(item.get('post_content_txt'))
        item['number'] = '0' * (path_len - len(str(count))) + str(count)
        count += 1
    print("[{}]--process data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def process_tianya_data(limit, min_num, max_num):
    print("[{}]--start process tianya data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    ty_article = get_tianya_data(limit, min_num, max_num)
    count = 0
    for item in ty_article:
        item['word_count'] = len(item.get('question_detail'))
        item['number'] = '0' * (path_len - len(str(count))) + str(count)
        count += 1
    print("[{}]--process tianya data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def process_sohu_data(limit, min_num, max_num):
    print("[{}]--start process sohu data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_article, bzy_sohu_article = get_sohu_data(limit, min_num, max_num)
    start(sohu_article)
    sohu_result = []
#     print(sj_sohu_result[-1])
    sohu_result += sj_sohu_result
#     print(sohu_result)
    # 开始处理sohu bzy数据并合并到数组
#     bzy_result = []
    for element in bzy_sohu_article:
        temp = {}
        temp['id'] = element.get('id')
        temp['time'] = time_util.date_to_stamp(element.get('time'))
        temp['article_link'] = ''
        temp['article_title'] = element.get('title')
        temp['article_content'] = element.get('content')
        temp['article_author'] = ''
        temp['article_avatar'] = ''
        temp['views_count'] = 0
        temp['article_publish_time'] = 0
        temp['article_topics'] = ''
        temp['article_thumbnails'] = ''
        temp['article_category'] = ''
        temp['article_content_txt'] = element.get('content')
        
        sohu_result.append(temp)
    count = 0
    for item in sohu_result:
        item['word_count'] = len(item.get('article_content_txt'))
        item['number'] = '0' * (path_len - len(str(count))) + str(count)
        count += 1
#     print(sohu_result[-1])
    print("[{}]--process sohu data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_result


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
            element['article_content_txt'] = temp
            sj_sohu_result.append(element)
            count += 1
        print("[{}]--process end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start(sohu_article, step=5000):
    temp_list = [sohu_article[i:i + step] for i in range(0, len(sohu_article), step)]
    thr_list = [Thread(i, temp_list[i]) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


def main(limit, min_num, max_num):
    # 清空数据库
    sql.execute("truncate table sina")
    sql.execute("truncate table sohu")
    sql.execute("truncate table tianya")
    
    sina_data, sohu_data, tianya_data = process_sina_data(limit, min_num, max_num), process_sohu_data(limit, min_num, max_num), process_tianya_data(
        limit, min_num, max_num)
    sohu_str = "insert into sohu(id, time, article_link, article_title, article_content, article_author, article_avatar, views_count, article_publish_time, article_topics, article_thumbnails, article_category, article_content_txt, word_count, number) values (%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)"
    sina_str = "insert sina(id, time, url, userid, nickname, avatar, follow_count, followers_count, post_time, post_content, post_content_txt, source, reposts_count, comments_count, attitudes_count, isLongText, pics, video, video_pic, is_repost, origin, reposts, comments, topic, word_count, number) values(%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)"
    tianya_str = "insert into tianya(id, question_link, question_title, get_time, question_detail, question_author, question_author_avatar, question_publish_time, question_topics, question_answer, word_count, number) values(%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s)"
    
    sohu_result = []
    for element in sohu_data:
        sohu_result.append(tuple(element.values()))
    
    sina_result = []
    for element in sina_data:
        sina_result.append(tuple(element.values()))
    
    tianya_result = []
    for element in tianya_data:
        tianya_result.append(tuple(element.values()))
    
    sohu_count = sql.insertmany(sohu_str, sohu_result)
    query_sohu = sql.queryone("select count(*) from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + str(min_num)
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + str(max_num) + "") + sql.queryone("select count(*) from bzy_sohu_article where CHAR_LENGTH(TRIM(content)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(content)) < " + str(max_num) + "")

    
    if sohu_count == query_sohu:
        print("write sohu data success...")
    else:
        print("write sohu data faild...")
        sys.exit(0)
        
    sina_count = sql.insertmany(sina_str, sina_result)
    query_sina = sql.queryone("select count(*) from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + str(max_num) + "")
    if sina_count == query_sina:
        print("write sina data success...")
    else:
        print("write sina data faild...")
        sys.exit(0)
    
    tianya_count = sql.insertmany(tianya_str, tianya_result)
    query_tianya = sql.queryone("select count(*) from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + str(max_num) + "")
    if tianya_count == query_tianya:
        print("write tianya data success...")
    else:
        print("write tianya data faild...")
        sys.exit(0)

if __name__ == '__main__':
    main(0, 80, 1800)
