#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-18 16:47
@Author  : red
@Site    : 
@File    : process_data.py
@Software: PyCharm
"""
from utils import sql_util as sql
import json
import uuid
import time


def sina_data():
	print("[{}]--start process sina!".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
	sql.execute("truncate table sj_sina_article")
	sql.execute("truncate table sj_sina_comment")
	print("[{}]--truncate table finally!".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))

	article = []
	comment = []
	result = sql.queryall(
		# "select * from sj_sina where isLongText = 'False' and is_repost = 'false' and comments <> '[]' limit %s", 200)
		"select * from sj_sina")
	for item1 in result:
		article_id = str(uuid.uuid4())
		temp = [article_id, item1.get('url'), item1.get('post_time'), item1.get('nickname'), item1.get('post_time'),
				item1.get('post_content_txt'), item1.get('reposts_count'), item1.get('comments_count'),
				item1.get('attitudes_count'), item1.get('topic')]

		article.append(temp)
		for item in json.loads(item1.get('comments')):
			temp = [str(uuid.uuid4()), article_id, item.get('comment_userid'), item.get('comment_nickname'),
					item.get('comment_content'), item.get('comment_attitudes_count'), item.get('comment_time'),
					item.get('comment_source')]
			comment.append(temp)
	print("[{}]--data integration finally!".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
	# 添加数据到数据库
	insert_article_sql = 'insert into sj_sina_article(id, url, time, nickname, post_time, post_content_txt,' \
						 ' reposts_count, comments_count, attitudes_count, topic)' \
						 ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	insert_comment_sql = 'insert into sj_sina_comment(id, article_id, comment_userid, comment_nickname,' \
						 ' comment_content, comment_attitudes_count, comment_time, comment_source)' \
						 ' values(%s, %s, %s, %s, %s, %s, %s, %s)'

	cnt = sql.insertmany(insert_article_sql, article)
	print("[{}]--article data insert to sql success. data count is {}.".format(
		time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()), cnt))
	cnt = sql.insertmany(insert_comment_sql, comment)
	print("[{}]--comment data insert to sql success. data count is {}.".format(
		time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()), cnt))


def tianya_data():
	print("[{}]--start process tianya!".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
	sql.execute("truncate table sj_tianya_article")
	sql.execute("truncate table sj_tianya_comment")
	print("[{}]--truncate table finally!".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))

	count_sql_str = "select count(*) from sj_tianya"
	num = sql.queryone(count_sql_str)
	step = 1000
	count = 0
	for i in range(int(num / step)):
		article = []
		comment = []
		# result = sql.queryall("select * from sj_tianya where question_link <> '[]' and length(question_detail)>75 limit %s",
		# 					  200)
		result = sql.queryall("select * from sj_tianya limit %s, %s", ((count + 1), (count + step)))
		count += step
		for item1 in result:
			article_id = str(uuid.uuid4())
			temp = [article_id, item1.get('question_title'), item1.get('get_time'), item1.get('question_detail'),
					item1.get('question_author'), item1.get('question_publish_time'), item1.get('question_topics'),
					item1.get('question_link')]

			article.append(temp)
			for item in json.loads(item1.get('question_answer')):
				temp = [str(uuid.uuid4()), article_id, item.get('question_answer_content'),
						item.get('question_answer_author'),
						item.get('question_answer_agree_count'), item.get('question_answer_publish_time')]
				comment.append(temp)
		print("[{}]--data integration finally!".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
		# 添加数据到数据库
		insert_article_sql = 'insert into sj_tianya_article(id, question_title, get_time, question_detail,' \
							 ' question_author, question_publish_time, question_topics, question_link)' \
							 ' values(%s, %s, %s, %s, %s, %s, %s, %s)'
		insert_comment_sql = 'insert into sj_tianya_comment(id, article_id, question_answer_content, ' \
							 'question_answer_author, question_answer_agree_count, question_answer_publish_time)' \
							 ' values(%s, %s, %s, %s, %s, %s)'

		cnt = sql.insertmany(insert_article_sql, article)
		print("[{}]--{} article data insert to sql success. data count is {}."
			  .format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()), count, cnt))
		cnt = sql.insertmany(insert_comment_sql, comment)
		print("[{}]--{} comment data insert to sql success. data count is {}."
			  .format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()), count, cnt))


if __name__ == '__main__':
	# sina_data()
	tianya_data()
