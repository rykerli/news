#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-12 14:36
@Author  : red
@Site    : 
@File    : install_data.py
@Software: PyCharm
"""
import os
import pandas as pd
import time


def get_data(file_path):
	# 读csv数据，忽略header，分隔符为','
	rs = pd.read_csv(file_path, header=None, sep=',')
	# 转为list
	rs = rs.values.tolist()
	print(rs)
	# 数据有问题，comment是多行的，数据重复，要在这里处理
	for element in rs:
		print(element)
		break
		# 取注释
		# print(element[5])


def get_file_list(dir_path, file_list):
	# 如果是文件则添加进 fileList
	if os.path.isfile(dir_path):
		file_list.append(dir_path)
	elif os.path.isdir(dir_path):
		for s in os.listdir(dir_path):  # 如果是文件夹
			new_dir = os.path.join(dir_path, s)
			get_file_list(new_dir, file_list)

	return file_list


if __name__ == '__main__':
	path = "/Users/red/Desktop/temp/news/data/sohu_data"
	path_list = get_file_list(path, [])
	print('[{}]--path list length :{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), len(path_list)))

	for element in path_list:
		print(get_data(element))
		break
