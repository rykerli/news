#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-16 10:34
@Author  : red
@Site    : 
@File    : save_word_new.py
@Software: PyCharm
"""
from utils import sql_util as sql
from utils import docx_util as doc
import os
import time


def get_record():
    print('[{}]--start save word'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    result = []
    num = sql.queryone("select count(*) from bazhuayu_article")
    step = 100
    count = 0
    for i in range(int(num / step)):
        array = sql.queryall("select * from bazhuayu_article limit %s, %s", ((count + 1), (count + step)))
        count += step
        print("[{}]--{} data has get from databases......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count))
        for item in array:
            temp = []
            temp.append(item.get('title'))
            temp.append(item.get('time'))
            temp.append(item.get('content'))
            temp.append(item.get('read_num'))

            comment_array = sql.queryall("select * from bazhuayu_comment where article_id = %s", item.get('id'))
            comment = []
            for item1 in comment_array:
                temp1 = []
                temp1.append(item1.get('user'))
                temp1.append(item1.get('comment'))
                temp1.append(item1.get('comment_time'))
                temp1.append(item1.get('like_num'))

                comment.append(temp1)

            temp.append(comment)

            result.append(temp)
    print('[{}]--data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return result


if __name__ == '__main__':
    # 清空目录
    doc.path_exists("/Users/red/Desktop/temp/news/data/docx")

    result = get_record()
    for temp in result:
        doc.save_docx(temp, os.path.join("/Users/red/Desktop/temp/news/data/docx", temp[0] + ".docx"))
    print('[{}]--generation doc finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print('[{}]--final'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
