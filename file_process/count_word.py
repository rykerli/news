#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/16 4:50 PM
@Author  : red
@Site    : 
@File    : count_word.py
@Software: PyCharm
"""
import time
from utils import file_util as file
from utils import cartesian
from utils import dir_util
from utils import xlwt_util
import threading
import os

neg = file.read_file("../resource/vocabulary/negative.txt")
pos = file.read_file("../resource/vocabulary/positive.txt")
neg_vo = []
[neg_vo.append(element.replace('\n', '')) for element in
 file.read_file("../resource/vocabulary/negative_vocabulary.txt")]
sohu_result_path = "/Users/red/Desktop/temp/news/data/500data/sohu_result"
sina_result_path = "/Users/red/Desktop/temp/news/data/500data/sina_result"
tianya_result_path = "/Users/red/Desktop/temp/news/data/500data/tianya_result"


class WordCount:
    def __init__(self, path, result_dict):
        self._neg = neg
        self._pos = pos
        self._path = path
        self._result_dict = result_dict

    def count_word(self):
        data = "".join(file.read_file(self._path))
        for element in self._neg:
            element = element.replace('\n', '')
            result = data.count(element)
            if result != 0:
                self._result_dict[element] = result
        for element in self._pos:
            element = element.replace('\n', '')
            result = data.count(element)
            if result != 0:
                self._result_dict[element] = result
        return self._result_dict


class RemoveNegatives:
    def __init__(self, path, word_lst, count_word_result):
        self._neg_vo = neg_vo
        self._path = path
        self._words = word_lst
        self._file_data = "".join(file.read_file(path))
        self._count_word_result = count_word_result

    def remove_repeat_count(self):
        car = cartesian.CartesianProduct()
        car.add_data(self._neg_vo)
        car.add_data(self._words)
        p = car.build()
        # 拼接否定词和统计的结果
        word_list = []
        for item in p:
            word_list.append(("".join(item), item[1]))

        for word in word_list:
            if word[0] in self._file_data:
                self._count_word_result[word[1]] -= 1
        return self._count_word_result


def write_file(f_path, word_dict_data):
    for element in word_dict_data:
        # print(type(element))
        if element[1] != 0:
            file.write_append_file(f_path, str(element))


class Thread(threading.Thread):
    def __init__(self, num, lst, path):
        self._path = path
        self._num = num
        self._lst = lst
        super().__init__()

    def run(self):
        print("[{}]--write file start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._num, len(self._lst)))

        for element in self._lst:
            # 只统计单词，不管是否带有否定词
            words = WordCount(element, {})
            count_result = words.count_word()

            # 将带否定词的词语置为0(改为-1)
            remove_repeat = RemoveNegatives(element, list(count_result.keys()), count_result)
            finally_result = remove_repeat.remove_repeat_count()
            sorted_dict = sorted(finally_result.items(), key=lambda item: item[1], reverse=True)
            # print(sorted_dict)
            # 将结果集中不为0的值写入文件
            write_file(os.path.join(self._path, str.split(element, '/')[-1]), sorted_dict)
            xlwt_util.writeData(sorted_dict,
                                os.path.join(self._path, str.split(element, '/')[-1].split('.')[0] + '.csv'))
        print("[{}]--write file end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start(path, data, step=100):
    temp_list = [data[i:i + step] for i in range(0, len(data), step)]
    thr_list = [Thread(i, temp_list[i], path) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


if __name__ == '__main__':
    origin_path_list = ["/Users/red/Desktop/temp/news/data/500data/sina",
                        "/Users/red/Desktop/temp/news/data/500data/sohu",
                        "/Users/red/Desktop/temp/news/data/500data/tianya"]
    result_path_list = [sina_result_path, sohu_result_path, tianya_result_path]
    i = 0
    for element in origin_path_list:
        # 清空文件夹
        dir_util.remove_dir(result_path_list[i])
        # 获取sina所有文件
        file_list = file.get_file_list(element, [])
        start(result_path_list[i], file_list)
        i += 1
