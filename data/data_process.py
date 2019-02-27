#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-01-14 11:40
@Author  : red
@Site    :
@File    : data_process.py
@Software: PyCharm
"""
from utils import sql_util as sql
import time
import uuid


def get_all_data():
    # start = time.time()
    title_lst = sql.queryall("select title from origin_data GROUP BY title")
    # print("time is %s" % (time.time() - start))
    # print("data num is %s" % (sql.queryone("select count(*) from origin_data")))
    article = []
    comment = []
    for title in title_lst:
        array1 = []
        lst = sql.queryall("select * from origin_data where title = %s", title)
        article_id = str(uuid.uuid4())
        array1.append(article_id)
        array1.append(lst[0].get('title'))
        array1.append(lst[0].get('time'))
        array1.append(lst[0].get('content'))
        array1.append(lst[0].get('read_num'))
        article.append(array1)

        comment_lst = []
        for item in lst:
            if item.get('comment') in comment_lst:
                continue
            else:
                comment_lst.append(item.get('comment'))
                array2 = []
                array2.append(item.get('user'))
                array2.append(item.get('comment'))
                array2.append(item.get('comment_time'))
                array2.append(item.get('like_num'))
                array2.append(article_id)
                array2.append(str(uuid.uuid4()))
                comment.append(array2)
    return article, comment


def insert_data(article, comment):
    sql_str1 = "truncate table article"
    sql_str2 = "truncate table comment"
    sql.execute(sql_str1)
    sql.execute(sql_str2)
    sql_article = "insert into article(id, title, time, content, read_num) " \
                  "values (%s, %s, %s, %s, %s)"
    sql_comment = "insert into comment(user, comment, comment_time, like_num, article_id, id) " \
                  "values (%s, %s, %s, %s, %s, %s)"
    sql.insertmany(sql_article, article)
    sql.insertmany(sql_comment, comment)


if __name__ == '__main__':
    article, comment = get_all_data()
    print("数据获取完毕。。。。。。")
    insert_data(article, comment)
