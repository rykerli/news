#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-26 07:58
@Author  : red
@Site    : 
@File    : file_util.py
@Software: PyCharm
"""


def write_file(file_path, content):
	with open(file_path, 'w', encoding='utf8') as w:
		w.write(content)


def append_file(file_path, content):
	with open(file_path, 'a', encoding='utf8') as w:
		w.write(content)


def read_file(file_path):
	with open(file_path, 'r', encoding='utf8') as r:
		rs = r.readlines()
	return rs


if __name__ == '__main__':
	print(read_file('/Users/red/Desktop/temp/news/data/sj_data/all_data/article_txt.txt'))
