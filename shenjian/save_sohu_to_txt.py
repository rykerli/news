#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-25 21:21
@Author  : red
@Site    : 
@File    : save_sohu_to_txt.py
@Software: PyCharm
"""
import os
import time

from utils import file_util, sql_util as sql, xlwt_util, docx_util as doc, filter_tags_util


def get_record():
    filters = filter_tags_util.FilterTag()

    print('[{}]--start save word'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    article = []
    excel = []
    # num = sql.queryone("select count(*) from souhu limit 200")
    num = 200
    step = 100
    count = 0
    sum = 0
    for i in range(int(num / step)):
        array = sql.queryall("select * from souhu limit %s, %s", (count, (count + step)))
        count += step
        print("[{}]--{} data has get from databases......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count))
        for item in array:
            sum += 1
            txt_id = '0' * (5 - len(str(sum))) + str(sum)
            excel_temp = [txt_id, item.get('article_link'),
                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('time'))),
                          item.get('article_category')]
            temp = [filters.stripTagSimple(item.get('article_content'))]
            #  只有文章
            article.append(temp)

            # excel索引
            excel.append(excel_temp)
    print('[{}]--data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return article, excel


if __name__ == '__main__':
    article, excel = get_record()
    # article存储路径
    article_path = "/Users/red/Desktop/temp/news/data/sj_data/sohu_data/article_txt"
    doc.path_exists(article_path)

    for i in range(len(excel)):
        file_util.write_file(os.path.join(article_path, excel[i][0] + '.txt'), article[i][0])
    print('[{}]--file write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    title = ['文件编号', 'url', '时间', '分类']
    xlwt_util.save_xlwt(4, 'sheet1', title, excel, '/Users/red/Desktop/temp/news/data/sj_data/sohu_data/index.xls')
    print('[{}]--excel write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
