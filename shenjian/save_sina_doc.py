#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-23 16:09
@Author  : red
@Site    : 
@File    : save_sina_doc.py
@Software: PyCharm
"""
from utils import sql_util as sql
from utils import docx_util as doc
import os
import time


def sina_record():
    print('[{}]--start save word'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    result = []
    num = sql.queryone("select count(*) from sj_sina_article")
    step = 100
    count = 0
    for i in range(int(num / step)):
        array = sql.queryall("select * from sj_sina_article limit %s, %s", ((count + 1), (count + step)))
        count += step
        print("[{}]--{} data has get from databases......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count))
        for item in array:
            temp = [item.get('id'), item.get('nickname'), item.get('post_time'), item.get('post_content_txt'),
                    item.get('reposts_count'), item.get('comments_count'), item.get('attitudes_count')]

            comment_array = sql.queryall("select * from sj_sina_comment where article_id = %s", item.get('id'))
            comment = []
            for item1 in comment_array:
                temp1 = [item1.get('comment_nickname'), item1.get('comment_content'),
                         item1.get('comment_attitudes_count'), item1.get('comment_time'), item1.get('comment_source')]

                comment.append(temp1)

            temp.append(comment)

            result.append(temp)
    print('[{}]--data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return result


if __name__ == '__main__':
    # 清空目录
    doc.path_exists("/Users/red/Desktop/temp/news/data/sina/docx")

    result = sina_record()
    for temp in result:
        doc.save_sina_docx(temp, os.path.join("/Users/red/Desktop/temp/news/data/sina/docx", temp[0] + ".docx"))
    print('[{}]--generation doc finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print('[{}]--final'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
