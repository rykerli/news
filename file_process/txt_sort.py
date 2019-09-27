#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/27 5:07 PM
@Author  : red
@Site    : 
@File    : txt_sort.py
@Software: PyCharm
"""
import time
from utils import xlwt_util
from utils import dir_util

import os

from utils import file_util as file

neg_vo = file.read_file("../resource/vocabulary/negative.txt")
neg = []
[neg.append(element.replace('\n', '')) for element in
 neg_vo]
pos_vo = file.read_file("../resource/vocabulary/positive.txt")
pos = []
[pos.append(element.replace('\n', '')) for element in
 pos_vo]
sohu_result_path = "/Users/red/Desktop/temp/news/data/500data/sohu_result"
sina_result_path = "/Users/red/Desktop/temp/news/data/500data/sina_result"
tianya_result_path = "/Users/red/Desktop/temp/news/data/500data/tianya_result"

result_path_list = [sina_result_path, sohu_result_path, tianya_result_path]
result_path = "/Users/red/Desktop/temp/news/data/500data/discourse_sort"


def sort_file_by_pos_and_neg(file_lists, path):
    print("[{}]--start sort {} discourse......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), path))
    result = []
    for item in file_lists:
        (filepath, tempfilename) = os.path.split(item)
        temp = []
        [temp.append(eval(element)) for element in file.read_file(item)]

        # 统计消极、积极词语数量
        neg_count = 0
        pos_count = 0
        for item1 in temp:
            if item1[0] in neg:
                neg_count += 1
            if item1[0] in pos:
                pos_count += 1
        result.append((tempfilename, str(pos_count), str(neg_count)))
    pos_sorted_list = sorted(result, key=lambda item2: (item2[1], item2[2]), reverse=True)
    pos_sorted_list.insert(0, ("file name", 'positive number', 'negative number'))
    xlwt_util.writeData(pos_sorted_list,
                        os.path.join(result_path, path + '_pos_sort.csv'))
    neg_sorted_list = sorted(result, key=lambda item3: (item3[2], item3[1]), reverse=True)
    neg_sorted_list.insert(0, ("file name", 'positive number', 'negative number'))
    xlwt_util.writeData(neg_sorted_list,
                        os.path.join(result_path, path + '_neg_sort.csv'))
    print("[{}]--end sort {} discourse......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), path))


if __name__ == '__main__':
    # 清空文件夹
    dir_util.remove_dir(result_path)
    for element in result_path_list:
        # 获取sina所有文件
        file_list = file.get_file_list_end_with(element, [], file_end_with="txt")
        sort_file_by_pos_and_neg(file_list, element.split('/')[-1])
