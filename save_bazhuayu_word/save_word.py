#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-01-11 13:37
@Author  : red
@Site    : 
@File    : save_bazhuayu_word.py
@Software: PyCharm
"""
from utils import sql_util as sql
from collections import defaultdict
from utils import docx_util as doc
import os


def get_record():
    title = []
    result = []
    comment = defaultdict(list)
    # num = sql.queryone("select count(*) from origin_data")
    num = 21000
    step = 1000
    count = 0
    for i in range(int(num / step)):
        array = sql.queryall("select * from origin_data limit %s, %s", ((count + 1), (count + step)))
        count += step
        print("%s条数据读取完毕。。。。。。" % count)
        if i == 0:
            result1 = []
            title.append(array[0].get('title'))

            result1.append(array[0].get('title'))
            result1.append(array[0].get('time'))
            result1.append(array[0].get('content'))
            result1.append(array[0].get('readNum'))
            result.append(result1)

        for item in array:
            result_temp = []
            if item.get('title') not in title:
                title.append(item.get('title'))

                result_temp.append(item.get('title'))
                result_temp.append(item.get('time'))
                result_temp.append(item.get('content'))
                result_temp.append(item.get('readNum'))

                comment[item.get('title')].append(item.get('user'))
                comment[item.get('title')].append(item.get('comment'))
                comment[item.get('title')].append(item.get('commentTime'))
                comment[item.get('title')].append(item.get('likeNum'))

                result.append(result_temp)
            else:
                comment[item.get('title')].append(item.get('user'))
                comment[item.get('title')].append(item.get('comment'))
                comment[item.get('title')].append(item.get('commentTime'))
                comment[item.get('title')].append(item.get('likeNum'))
    return result, comment


if __name__ == '__main__':
    # 清空目录
    doc.path_exists("/Users/red/Desktop/temp/news/data/docx")

    result, comment = get_record()
    # print(comment)
    print(len(result))
    print("数据整合完毕。。。。。。")
    for item in result:
        if item[0] in list(comment.keys()):
            item.append(list(comment.get(item[0])))
    print("评论整合完毕。。。。。。")
    for temp in result:
        doc.save_docx(temp, os.path.join("/Users/red/Desktop/temp/news/data/docx", temp[0] + ".docx"))
    print("final")
