#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-01-07 08:57
@Author  : red
@Site    : 
@File    : seg_word.py
@Software: PyCharm
"""
import jieba_fast as jieba
import configparser as cf
import codecs
from utils import file_util

# 开启并行分词模式，参数为并行进程数
jieba.enable_parallel(4)


def get_file_path(section, key):
	conf = cf.ConfigParser()
	conf.read('../conf/config.cfg')
	return conf.get(section, key)


def get_stop_word():
	with codecs.open(get_file_path('stop_file', 'stop_words_chinese_1'), 'r', encoding='utf8') as f1:
		data1 = f1.read()

	with codecs.open(get_file_path('stop_file', 'stop_words_english_1'), 'r') as f2:
		data2 = f2.read()
	f_stop_list = (data1 + data2).split('\n')
	return f_stop_list


def write_file(file_path, content):
	with codecs.open(file_path, 'w', encoding='utf8') as w:
		w.write(u" ".join(content))


def split(stop_lists, data):
	word_list = []
	seg_list = jieba.cut(data, cut_all=False)
	list_str = " ".join(seg_list)

	for word in list_str.split(" "):
		if not (word.strip().lower() in stop_lists) and len(word.strip()) > 1:
			word_list.append(word)
	write_file("/Users/red/Desktop/temp/news/data/sj_data/all_data/all_seg_word_data.txt", word_list)


def get_content():
	return file_util.read_file("/Users/red/Desktop/temp/news/data/sj_data/all_data/all.txt")


if __name__ == '__main__':
	stop_word_list = get_stop_word()
	split(stop_word_list, get_content())
