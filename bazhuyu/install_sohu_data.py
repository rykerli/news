#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-12 14:36
@Author  : red
@Site    : 
@File    : install_sohu_data.py
@Software: PyCharm
"""
import os
import pandas as pd
import time
from utils import sql_util as sql


def get_data(file_path):
	# 读csv数据，忽略header，分隔符为',', skiprows跳过第0行
	rs = pd.read_csv(file_path, header=None, sep=',', skiprows=0, na_values=None, keep_default_na=False)
	# 转为list
	rs = rs.values.tolist()
	return rs


def get_file_list(dir_path, file_list):
	# 如果是文件则添加进 fileList
	if os.path.isfile(dir_path):
		file_list.append(dir_path)
	elif os.path.isdir(dir_path):
		for s in os.listdir(dir_path):  # 如果是文件夹
			new_dir = os.path.join(dir_path, s)
			get_file_list(new_dir, file_list)

	return file_list


def install_data_to_sql():
	data_sum = 0
	truncate_sql = "truncate table bzy_sohu_origin_data"
	sql.execute(truncate_sql)
	sql_str = 'insert into bzy_sohu_origin_data(title, time, content, user, comment) values (%s, %s, %s, %s, %s)'
	path = "/Users/red/Desktop/temp/news/data/sohu_data"
	path_list = get_file_list(path, [])
	print('[{}]--path list length :{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), len(path_list)))

	for element in path_list:
		result = get_data(element)
		sql.insertmany(sql_str, result)
		data_sum += len(result)
		print('[{}]--insert file {}, {} data to sql'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
													   element, len(result)))
	print('[{}]--insert all data, {} data to sql'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
														 data_sum))


if __name__ == '__main__':
	install_data_to_sql()
