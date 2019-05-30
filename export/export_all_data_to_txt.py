#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-30 17:20
@Author  : red
@Site    : 
@File    : export_all_data_to_txt.py
@Software: PyCharm
"""
from utils import sql_util as sql
from utils import file_util


def load_data():
	sql_str_sina_article = "select post_content_txt from sj_sina_article limit 100"
	sql_str_sina_comment = "select comment_content from sj_sina_comment limit 100"
	sql_str_tianya_article = "select question_detail from sj_tianya_article limit 100"
	sql_str_tianya_comment = "select question_answer_content from sj_tianya_comment limit 100"
	sql_str_sohu = "select article_content from sj_sohu limit 100"
	sql_str_sohu_bzy_article = "select content from bzy_sohu_article limit 100"
	sql_str_sohu_bzy_comment = "select comment from bzy_sohu_comment limit 100"

	sina_article_result = sql.queryall(sql_str_sina_article)
	sina_comment_result = sql.queryall(sql_str_sina_comment)
	tianya_article_result = sql.queryall(sql_str_tianya_article)
	tianya_comment_result = sql.queryall(sql_str_tianya_comment)
	sohu_result = sql.queryall(sql_str_sohu)
	sohu_bzy_article_result = sql.queryall(sql_str_sohu_bzy_article)
	sohu_bzy_comment_result = sql.queryall(sql_str_sohu_bzy_comment)

	return sina_article_result, sina_comment_result, tianya_article_result, tianya_comment_result, sohu_result, \
		   sohu_bzy_article_result, sohu_bzy_comment_result


if __name__ == '__main__':
	sina_article_result, sina_comment_result, tianya_article_result, tianya_comment_result, sohu_result, \
	sohu_bzy_article_result, sohu_bzy_comment_result = load_data()

	path = "/Users/red/Desktop/temp/news/data/sj_data/all_data/all.txt"
	for element in sina_article_result:
		file_util.append_file(path, str(element) + "\n")
	for element in sina_comment_result:
		file_util.append_file(path, str(element) + "\n")
	for element in tianya_article_result:
		file_util.append_file(path, str(element) + "\n")
	for element in tianya_comment_result:
		file_util.append_file(path, str(element) + "\n")
	for element in sohu_result:
		file_util.append_file(path, str(element) + "\n")
	for element in sohu_bzy_article_result:
		file_util.append_file(path, str(element) + "\n")
	for element in sohu_bzy_comment_result:
		file_util.append_file(path, str(element) + "\n")
