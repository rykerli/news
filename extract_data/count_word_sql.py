#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/16 4:50 PM
@Author  : red
@Site    : 
@File    : count_word.py
@Software: PyCharm
"""
import sys
sys.path.append('../utils')
import time
import file_util as file
import sql_util as sql
import cartesian
import threading
import os

neg_v = file.read_file("../resource/vocabulary/negative.txt")
neg = []
[neg.append(element.replace('\n', '')) for element in
 neg_v]
pos_v = file.read_file("../resource/vocabulary/positive.txt")
pos = []
[pos.append(element.replace('\n', '')) for element in
 pos_v]
neg_vo = []
[neg_vo.append(element.replace('\n', '')) for element in
 file.read_file("../resource/vocabulary/negative_vocabulary.txt")]


class WordCount:
    def __init__(self, data, result_dict):
        self._neg = neg
        self._pos = pos
        self._data = data
        self._result_dict = result_dict

    def count_word(self):
        data = self._data
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
    def __init__(self, data, word_lst, count_word_result):
        self._neg_vo = neg_vo
        self._data = data
        self._words = word_lst
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
            if word[0] in self._data:
                self._count_word_result[word[1]] -= 1
        return self._count_word_result


class Thread(threading.Thread):
    def __init__(self, num, lst, path):
        self._path = path
        self._num = num
        self._lst = lst
        super().__init__()

    def run(self):
        print("[{}]--update count word start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._num, len(self._lst)))

        for element in self._lst:
            # 只统计单词，不管是否带有否定词
            if self._path == "sina":
                words = WordCount(element.get('post_content_txt'), {})
                count_result = words.count_word()
                 # 将带否定词的词语置为0(改为-1)
                remove_repeat = RemoveNegatives(element.get('post_content_txt'), list(count_result.keys()), count_result)
                finally_result = remove_repeat.remove_repeat_count()
                sorted_dict = sorted(finally_result.items(), key=lambda item: item[1], reverse=True)
                sql.execute("update "+ self._path + " set pn_word_count = %s where id = %s", (str(sorted_dict), element.get('id')))
            elif self._path == "sohu":
                words = WordCount(element.get('article_content_txt'), {})
                count_result = words.count_word()
                 # 将带否定词的词语置为0(改为-1)
                remove_repeat = RemoveNegatives(element.get('article_content_txt'), list(count_result.keys()), count_result)
                finally_result = remove_repeat.remove_repeat_count()
                sorted_dict = sorted(finally_result.items(), key=lambda item: item[1], reverse=True)
                sql.execute("update "+ self._path + " set pn_word_count = %s where id = %s", (str(sorted_dict), element.get('id')))
            else:
                words = WordCount(element.get('question_detail'), {})
                count_result = words.count_word()
                 # 将带否定词的词语置为0(改为-1)
                remove_repeat = RemoveNegatives(element.get('question_detail'), list(count_result.keys()), count_result)
                finally_result = remove_repeat.remove_repeat_count()
                sorted_dict = sorted(finally_result.items(), key=lambda item: item[1], reverse=True)
                # 将结果集中不为0的数据更新到数据库
                sql.execute("update "+ self._path + " set pn_word_count = %s where id = %s", (str(sorted_dict), element.get('id')))

        print("[{}]--update count word end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start(path, data, step=5000):
    temp_list = [data[i:i + step] for i in range(0, len(data), step)]
    thr_list = [Thread(i, temp_list[i], path) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]



def update_positive_negative_word_num(sina_pn_data, sohu_pn_data, tianya_pn_data):
    print("[{}]--start update sina positive_negative_number......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    for element in sina_pn_data:
        temp = eval(element.get('pn_word_count'))
        # 统计消极、积极词语数量、文章字数
        neg_count = 0
        pos_count = 0
        for item in temp:
            if item[0] in neg:
                neg_count += item[1]
            if item[0] in pos:
                pos_count += item[1]
        sql.execute("update sina set positive_number = %s, negative_number = %s where id = %s", (pos_count, neg_count, element.get('id')))
    print("[{}]--start update sina positive_negative_number......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    print("[{}]--start update sohu positive_negative_number......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    for element in sohu_pn_data:
        temp = eval(element.get('pn_word_count'))
        
        # 统计消极、积极词语数量、文章字数
        neg_count = 0
        pos_count = 0
        for item in temp:
            if item[0] in neg:
                neg_count += item[1]
            if item[0] in pos:
                pos_count += item[1]
        sql.execute("update sohu set positive_number = %s, negative_number = %s where id = %s", (pos_count, neg_count, element.get('id')))
    print("[{}]--start update sohu positive_negative_number......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    print("[{}]--start update tianya positive_negative_number......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    for element in tianya_pn_data:
        temp = eval(element.get('pn_word_count'))
        
        # 统计消极、积极词语数量、文章字数
        neg_count = 0
        pos_count = 0
        for item in temp:
            if item[0] in neg:
                neg_count += item[1]
            if item[0] in pos:
                pos_count += item[1]
        sql.execute("update tianya set positive_number = %s, negative_number = %s where id = %s", (pos_count, neg_count, element.get('id')))
    print("[{}]--start update tianya positive_negative_number......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    

def get_data():
    print("[{}]--start get sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    sina_data = sql.queryall("select id, post_content_txt from sina")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    print("[{}]--start get sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_data = sql.queryall("select id, article_content_txt from sohu")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    print("[{}]--start get tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    tianya_data = sql.queryall("select id, question_detail from tianya")
    
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_data, sohu_data, tianya_data


def get_pn_data():
    print("[{}]--start get sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    sina_data = sql.queryall("select id, pn_word_count from sina")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    print("[{}]--start get sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_data = sql.queryall("select id, pn_word_count from sohu limit")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    print("[{}]--start get tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    tianya_data = sql.queryall("select id, pn_word_count from tianya limit")
    
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_data, sohu_data, tianya_data
    
    
def start_main():
    sina_data, sohu_data, tianya_data = get_data()
#     origin_data = [sina_data, sohu_data, tianya_data]
#     result_list = ["sina", "sohu", "tianya"]
    
#     i = 0
#     for element in origin_data:
#         print("[{}]--update count {} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), result_list[i]))
#         start(result_list[i], origin_data[i])
#         print("[{}]--update count {} data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), result_list[i]))
#         i += 1
    sina_pn_data, sohu_pn_data, tianya_pn_data = get_pn_data()
    update_positive_negative_word_num(sina_pn_data, sohu_pn_data, tianya_pn_data)
    
    
if __name__ == '__main__':
    start_main()