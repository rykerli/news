#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/11/14 4:48 PM
@Author  : red
@Site    : 
@File    : data_update.py
@Software: PyCharm
"""
import time
import os
import sys
sys.path.append('../utils')
import sql_util as sql
import dir_util
import file_util
import jieba_fast.posseg as jieba
import configparser as cf
import codecs
import re

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


def split(path1, path2, data):
    stop_lists = get_stop_word()
    word_list = []
    seg_list = jieba.cut(data)

    for word in seg_list:
        if not (word.word.strip().lower() in stop_lists) \
                and len(word.word.strip()) > 1 \
                and not word.word.isdigit() \
                and not re.search('[a-zA-Z]', word.word) \
                and '\u4e00' <= word.word <= '\u9fff':
            word_list.append(word.word + '/' + word.flag)
    for element in word_list:
        file_util.append_file(path1, element + '\n')
    data = re.sub('\s', '', data)
    file_util.write_file(path2, data)
    
    
def ready_data(path, table, table_type):
    if table == "sina":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        sina_data = sql.queryall("select number, positive_number, negative_number, word_count, pn_word_count, post_content_txt, order_pos, order_neg, order_nou from sina where "+ table_type +"_status = 0 and order_" + table_type + " is not null")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type + "_seg_word"))
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type + "_remove_useless"))
        # 将数据写入txt文件
        for element in sina_data:
            path1 = os.path.join(path, table, table + "_" + table_type + "_seg_word", str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt")
            path2 = os.path.join(path, table, table + "_" + table_type + "_remove_useless", str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt")
            split(path1, path2, element.get('post_content_txt'))

        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "sohu":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        sohu_data_count = 0
        sohu_data = sql.queryall("select number, positive_number, negative_number, word_count, pn_word_count, article_content_txt, order_pos, order_neg, order_nou from sohu where "+ table_type + "_status = 0 and order_" + table_type + " is not null")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type + "_seg_word"))
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type + "_remove_useless"))
        # 将数据写入txt文件
        for element in sohu_data:
            path1 = os.path.join(path, table, table + "_" + table_type + "_seg_word", str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt")
            path2 = os.path.join(path, table, table + "_" + table_type + "_remove_useless", str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt")
            split(path1, path2, element.get('article_content_txt'))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "tianya":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        tianya_data = sql.queryall("select number, positive_number, negative_number, word_count, pn_word_count, question_detail, order_pos, order_neg, order_nou from tianya where "+ table_type +"_status = 0 and order_" + table_type + " is not null")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type + "_seg_word"))
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type + "_remove_useless"))
        # 将数据写入txt文件
        for element in tianya_data:
            path1 = os.path.join(path, table, table + "_" + table_type + "_seg_word", str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt")
            path2 = os.path.join(path, table, table + "_" + table_type + "_remove_useless", str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt")
            split(path1, path2, element.get('question_detail'))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
    
        
if __name__ == '__main__':
    ready_data("/home/ftpUser/pub/update", "sina", "pos")
    ready_data("/home/ftpUser/pub/update", "sina", "neg")
    ready_data("/home/ftpUser/pub/update", "sina", "nou")
    
    ready_data("/home/ftpUser/pub/update", "sohu", "pos")
    ready_data("/home/ftpUser/pub/update", "sohu", "neg")
    ready_data("/home/ftpUser/pub/update", "sohu", "nou")
    
    ready_data("/home/ftpUser/pub/update", "tianya", "pos")
    ready_data("/home/ftpUser/pub/update", "tianya", "neg")
    ready_data("/home/ftpUser/pub/update", "tianya", "nou")