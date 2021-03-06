#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/27 5:07 PM
@Author  : red
@Site    : 
@File    : txt_sort.py
@Software: PyCharm
"""
import sys
sys.path.append('../utils')
import time
import xlwt_util
import dir_util

import os

import file_util as file

neg_vo = file.read_file("../resource/vocabulary/negative.txt")
neg = []
[neg.append(element.replace('\n', '')) for element in
 neg_vo]
pos_vo = file.read_file("../resource/vocabulary/positive.txt")
pos = []
[pos.append(element.replace('\n', '')) for element in
 pos_vo]
# sohu_result_path = "/root/data/news/500data/sohu_result"
# sina_result_path = "/root/data/news/500data/sina_result"
# tianya_result_path = "/root/data/news/500data/tianya_result"
sohu_result_path = "/home/data/news/80data/sohu_result"
sina_result_path = "/home/data/news/80data/sina_result"
tianya_result_path = "/home/data/news/80data/tianya_result"

result_path_list = [sina_result_path, sohu_result_path, tianya_result_path]
result_path = "/home/data/news/80data/discourse_sort"


def sort_file_by_pos_and_neg(file_lists, path):
    print("[{}]--start sort {} discourse......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), path))
    result = []
    for item in file_lists:
        (filepath, tempfilename) = os.path.split(item)
        temp = []
        [temp.append(eval(element)) for element in file.read_file(item)]

        # 统计消极、积极词语数量、文章字数
        neg_count = 0
        pos_count = 0
#         txt_sum = 0
        for item1 in temp:
            if item1[0] in neg:
                neg_count += 1
            if item1[0] in pos:
                pos_count += 1
#             txt_sum += len(item1)
        result.append((tempfilename, str(pos_count), str(neg_count)))
    pos_sorted_list = sorted(result, key=lambda item2: (int(item2[1]), int(item2[2])), reverse=True)
    pos_sorted_list.insert(0, ("file name", 'positive number', 'negative number'))
    xlwt_util.writeData(pos_sorted_list,
                        os.path.join(result_path, path + '_pos_sort.csv'))
    neg_sorted_list = sorted(result, key=lambda item3: (int(item3[2]), int(item3[1])), reverse=True)
    neg_sorted_list.insert(0, ("file name", 'positive number', 'negative number'))
    xlwt_util.writeData(neg_sorted_list,
                        os.path.join(result_path, path + '_neg_sort.csv'))
    print("[{}]--end sort {} discourse......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), path))


def start():
    # 清空文件夹
    dir_util.remove_dir(result_path)
    for element in result_path_list:
        # 获取sina所有文件
        file_list = file.get_file_list_end_with(element, [], file_end_with="txt")
        sort_file_by_pos_and_neg(file_list, element.split('/')[-1])
