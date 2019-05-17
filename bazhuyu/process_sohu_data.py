#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-17 11:20
@Author  : red
@Site    : 
@File    : process_sohu_data.py
@Software: PyCharm
"""
from utils import sql_util as sql
import time
import uuid


def get_all_data():
	title_lst = sql.queryall("select title from bzy_sohu_origin_data GROUP BY title")
	print('[{}]--get data group by title'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	article = []
	comment = []
	for title in title_lst:
		array1 = []
		lst = sql.queryall("select * from bzy_sohu_origin_data where title = %s", title)
		article_id = str(uuid.uuid4())
		array1.append(article_id)
		array1.append(lst[0].get('title'))
		array1.append(lst[0].get('time'))
		array1.append(lst[0].get('content'))
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
				array2.append(article_id)
				array2.append(str(uuid.uuid4()))
				comment.append(array2)
	print('[{}]--process data finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	return article, comment


def install_sql():
	print('[{}]--install sql start'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	article, comment = get_all_data()
	sql_str1 = "truncate table bzy_sohu_article"
	sql_str2 = "truncate table bzy_sohu_comment"
	sql.execute(sql_str1)
	sql.execute(sql_str2)
	sql_article = "insert into bzy_sohu_article(id, title, time, content) " \
				  "values (%s, %s, %s, %s)"
	sql_comment = "insert into bzy_sohu_comment(user, comment, article_id, id) " \
				  "values (%s, %s, %s, %s)"
	sql.insertmany(sql_article, article)
	sql.insertmany(sql_comment, comment)
	print('[{}]--install sql end'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


if __name__ == '__main__':
	install_sql()
