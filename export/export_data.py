#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-17 09:05
@Author  : red
@Site    : 
@File    : export_data.py
@Software: PyCharm
"""
import time
from utils import file_util, sql_util as sql, xlwt_util, docx_util as doc, filter_tags_util
import os


def get_data():
	filters = filter_tags_util.FilterTag()
	print('[{}]--start save word'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	# 处理sina数据
	sina_article_comment = []
	sina_article = []
	sina_excel = []
	step = 100
	sina_num = sql.queryone("select count(*) from sj_sina_article")
	sina_count = 0
	sina_sum = 0
	for i in range(int(sina_num / step)):
		array = sql.queryall("select * from sj_sina_article limit %s, %s", (sina_count, (sina_count + step)))
		sina_count += step
		print("[{}]--{} sina data has get from database......".format(
			time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), sina_count))
		for item in array:
			sina_sum += 1
			txt_id = 'sina' + '0' * (5 - len(str(sina_sum))) + str(sina_sum)
			sina_excel_temp = [txt_id, item.get('url'), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get(
				'time'))),
							   item.get('topic')]
			sina_temp = [item.get('post_content_txt'), txt_id]

			sina_comment_array = sql.queryall("select * from sj_sina_comment where article_id = %s", item.get('id'))
			sina_temp_filter = ''
			for item1 in sina_comment_array:
				temp1 = [item1.get('comment_content')]
				for item2 in temp1:
					sina_temp_filter += (filters.stripTagSimple(item2) + '\r')

			#  只有文章
			sina_article.append(sina_temp)

			sina_temp.append(sina_temp_filter)
			# 文章加评论
			sina_article_comment.append(sina_temp)
			# excel索引
			sina_excel.append(sina_excel_temp)
	print('[{}]--sina data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	# 处理天涯数据
	ty_article_comment = []
	ty_article = []
	ty_excel = []
	ty_num = sql.queryone("select count(*) from sj_tianya_article")
	ty_count = 0
	ty_sum = 0
	for i in range(int(ty_num / step)):
		ty_array = sql.queryall("select * from sj_tianya_article limit %s, %s", (ty_count, (ty_count + step)))
		ty_count += step
		print("[{}]--{} tianya data has get from database......".format(
			time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ty_count))
		for item in ty_array:
			ty_sum += 1
			txt_id = 'ty' + '0' * (5 - len(str(ty_sum))) + str(ty_sum)
			ty_excel_temp = [txt_id, item.get('question_link'),
							 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(item.get('question_publish_time')))),
							 item.get('question_topics')]
			ty_temp = [item.get('question_detail'), txt_id]

			ty_comment_array = sql.queryall("select * from sj_tianya_comment where article_id = %s", item.get('id'))
			ty_temp_filter = ''
			for item1 in ty_comment_array:
				temp1 = [item1.get('question_answer_content')]
				for item2 in temp1:
					ty_temp_filter += (filters.stripTagSimple(item2) + '\r')

			#  只有文章
			ty_article.append(ty_temp)

			ty_temp.append(ty_temp_filter)
			# 文章加评论
			ty_article_comment.append(ty_temp)
			# excel索引
			ty_excel.append(ty_excel_temp)
	print('[{}]--tianya data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	# 处理sohu数据
	sohu_article = []
	sohu_excel = []
	# num = sql.queryone("select count(*) from souhu limit 200")
	sohu_num = 200
	sohu_count = 0
	sohu_sum = 0
	for i in range(int(sohu_num / step)):
		array = sql.queryall("select * from sj_sohu limit %s, %s", (sohu_count, (sohu_count + step)))
		sohu_count += step
		print("[{}]--{} sohu data has get from databases......".format(
			time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), sohu_count))
		for item in array:
			sohu_sum += 1
			txt_id = '0' * (5 - len(str(sohu_sum))) + str(sohu_sum)
			sohu_excel_temp = [txt_id, item.get('article_link'),
							   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get('time'))),
							   item.get('article_category')]
			sohu_temp = [filters.stripTagSimple(item.get('article_content')), txt_id]
			#  只有文章
			sohu_article.append(sohu_temp)

			# excel索引
			sohu_excel.append(sohu_excel_temp)
	print('[{}]--sohu data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	print('[{}]--data process finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	return sina_article_comment, sina_article, sina_excel, ty_article_comment, ty_article, ty_excel, sohu_article, \
		   sohu_article, sohu_excel


def save_data():
	sina_article_comment, sina_article, sina_excel, ty_article_comment, ty_article, ty_excel, sohu_article_comment, \
	sohu_article, sohu_excel = get_data()

	# article存储路径
	article_path = "/Users/red/Desktop/temp/news/data/sj_data/all_data/article_txt.txt"
	article_docx_path = "/Users/red/Desktop/temp/news/data/sj_data/all_data/article.docx"
	# doc.path_exists(article_path)
	# article_comment存储路径
	article_comment_path = "/Users/red/Desktop/temp/news/data/sj_data/all_data/article_comment_txt.txt"
	article_comment_docx_path = "/Users/red/Desktop/temp/news/data/sj_data/all_data/article_comment.docx"
	# doc.path_exists(article_comment_path)

	# sina数据保存
	for i in range(len(sina_excel)):
		file_util.append_file(article_path, sina_article[i][1] + '\n\n')
		file_util.append_file(article_path, sina_article[i][0] + '\n\n')
		file_util.append_file(article_path, '\n\n')
		file_util.append_file(article_comment_path, sina_article_comment[i][1] + '\n\n')
		file_util.append_file(article_comment_path,
							  str(sina_article_comment[i][0]) + '\n\n' + str(sina_article_comment[i][2]))
		file_util.append_file(article_comment_path, '\n\n')
	print('[{}]--sina file write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	title = ['文件编号', 'url', '时间', '话题']
	xlwt_util.save_xlwt(4, 'sheet1', title, sina_excel,
						'/Users/red/Desktop/temp/news/data/sj_data/all_data/sj_data_index/sina_index.xls')
	print('[{}]--sina excel write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	# tianya数据保存
	for i in range(len(ty_excel)):
		file_util.append_file(article_path, ty_article[i][1] + '\n\n')
		file_util.append_file(article_path, ty_article[i][0] + '\n\n')
		file_util.append_file(article_path, '\n\n')
		file_util.append_file(article_comment_path, ty_article_comment[i][1] + '\n\n')
		file_util.append_file(article_comment_path,
							  str(ty_article_comment[i][0]) + '\n\n' + str(ty_article_comment[i][2]))
		file_util.append_file(article_comment_path, '\n\n')
	print('[{}]--tianya file write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	title = ['文件编号', 'url', '时间', '话题']
	xlwt_util.save_xlwt(4, 'sheet1', title, ty_excel,
						'/Users/red/Desktop/temp/news/data/sj_data/all_data/sj_data_index/tianya_index.xls')
	print('[{}]--tianya excel write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	# sohu数据保存
	# article存储路径

	for i in range(len(sohu_excel)):
		file_util.append_file(article_path, sohu_article[i][1] + '\n\n')
		file_util.append_file(article_path, sohu_article[i][0] + '\n\n')
		file_util.append_file(article_path, '\n\n')
		file_util.append_file(article_comment_path, sohu_article_comment[i][1] + '\n\n')
		file_util.append_file(article_comment_path,
							  str(sohu_article_comment[i][0]) + '\n\n')
		file_util.append_file(article_comment_path, '\n\n')
	print('[{}]--sohu file write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	title = ['文件编号', 'url', '时间', '分类']
	xlwt_util.save_xlwt(4, 'sheet1', title, sohu_excel,
						'/Users/red/Desktop/temp/news/data/sj_data/all_data/sj_data_index/sohu_index.xls')
	print('[{}]--sohu excel write finally'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

	# 将txt导入word
	doc.save_content_to_docx(article_docx_path, file_util.read_file(article_path))
	doc.save_content_to_docx(article_comment_docx_path, file_util.read_file(article_comment_path))


if __name__ == '__main__':
	save_data()
