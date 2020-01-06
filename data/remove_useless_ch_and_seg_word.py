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


def split(data):
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
#     for element in word_list:
#         file_util.append_file(path1, element + '\n')
#     data = re.sub('\s', '', data)
#     file_util.write_file(path2, data)
    return word_list, re.sub('\s', '', data)
    
# result1:标注后的词语 result2:去除空格后的原文
def identifier_txt(result1, result2):
    result_str = ''
    flag = 0
    len_str = len(result2)
    for element in (result1): 
        # 取词语
        s = re.sub('/.*$', '', element).strip()
    #     print(s)
        # 取标识符
        identifier = re.sub('^([^/]*)', '', element)
        result2 = result2[flag:len_str]
    #     print(result2)
    #     print(result2[0:result2.find(s) + len(s)])
        result_str += result2[0:result2.find(s) + len(s)]
        flag = result2.find(s) + len(s)
    #     print(flag)
        result_str += identifier.strip()
    return result_str

    
def ready_data(table, table_type):
    if table == "sina":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        sina_data = sql.queryall("select number, positive_number, negative_number, word_count, pn_word_count, post_content_txt, order_pos, order_neg, order_nou from sina where "+ table_type +"_status = 0 and order_" + table_type + " is not null")

        for element in sina_data:
            data1, data2 = split(element.get('post_content_txt'))
            result = identifier_txt(data1, data2)
            sql.execute('update ' + table + ' set remove_useless = %s, identifier_txt = %s where number = %s ', (data2, result, element.get('number')))
            
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "sohu":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        sohu_data = sql.queryall("select number, positive_number, negative_number, word_count, pn_word_count, article_content_txt, order_pos, order_neg, order_nou from sohu where "+ table_type + "_status = 0 and order_" + table_type + " is not null")

        # 将数据写入txt文件
        for element in sohu_data:
            data1, data2 = split(element.get('article_content_txt'))
            result = identifier_txt(data1, data2)
            sql.execute('update ' + table + ' set remove_useless = %s, identifier_txt = %s where number = %s ', (data2, result, element.get('number')))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "tianya":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        tianya_data = sql.queryall("select number, positive_number, negative_number, word_count, pn_word_count, question_detail, order_pos, order_neg, order_nou from tianya where "+ table_type +"_status = 0 and order_" + table_type + " is not null")

        # 将数据写入txt文件
        for element in tianya_data:
            data1, data2 = split(element.get('question_detail'))
            result = identifier_txt(data1, data2)
            sql.execute('update ' + table + ' set remove_useless = %s, identifier_txt = %s where number = %s ', (data2, result, element.get('number')))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
    
        
if __name__ == '__main__':
    ready_data("sina", "pos")
    ready_data("sina", "neg")
    ready_data("sina", "nou")
    
    ready_data("sohu", "pos")
    ready_data("sohu", "neg")
    ready_data("sohu", "nou")
    
    ready_data("tianya", "pos")
    ready_data("tianya", "neg")
    ready_data("tianya", "nou")