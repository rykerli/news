#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-25 21:19
@Author  : red
@Site    : 
@File    : save_sina_to_txt.py
@Software: PyCharm
"""
import os
import time
import json

from utils import file_util, sql_util as sql, xlwt_util, docx_util as doc, filter_tags_util


def get_record():
    filters = filter_tags_util.FilterTag()

    print('[{}]--start save word'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    article_comment = []
    article = []
    excel = []
    num = sql.queryone("select count(*) from sj_sina_article")
    step = 100
    count = 0
    sum = 0
    for i in range(int(num / step)):
        array = sql.queryall("select * from sj_sina_article limit %s, %s", (count, (count + step)))
        count += step
        print("[{}]--{} data has get from databases......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count))
        for item in array:
            sum += 1
            txt_id = '0' * (5 - len(str(sum))) + str(sum)
            excel_temp = [txt_id, item.get('url'), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('time'))),
                          item.get('topic')]
            temp = [item.get('post_content_txt')]

            comment_array = sql.queryall("select * from sj_sina_comment where article_id = %s", item.get('id'))
            temp_filter = ''
            for item1 in comment_array:
                temp1 = [item1.get('comment_content')]
                for item2 in temp1:
                    temp_filter += (filters.stripTagSimple(item2) + '\r')

            #  只有文章
            article.append(temp)

            temp.append(temp_filter)
            # 文章加评论
            article_comment.append(temp)
            # excel索引
            excel.append(excel_temp)
    print('[{}]--data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return article_comment, article, excel


if __name__ == '__main__':
    article_comment, article, excel = get_record()
    # article存储路径
    article_path = "/Users/red/Desktop/temp/news/data/sj_data/sina_data/article_txt"
    doc.path_exists(article_path)
    # article_comment存储路径
    article_comment_path = "/Users/red/Desktop/temp/news/data/sj_data/sina_data/article_comment_txt"
    doc.path_exists(article_comment_path)

    for i in range(len(excel)):
        file_util.write_file(os.path.join(article_path, excel[i][0] + '.txt'), article[i][0])
        file_util.write_file(os.path.join(article_comment_path, excel[i][0] + '.txt'),
                             str(article_comment[i][0]) + '\n\n' + str(article_comment[i][1]))
    print('[{}]--file write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    title = ['文件编号', 'url', '时间', '话题']
    xlwt_util.save_xlwt(4, 'sheet1', title, excel, '/Users/red/Desktop/temp/news/data/sj_data/sina_data/index.xls')
    print('[{}]--excel write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
