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
import file_util
import dir_util
import xlwt_util


finally_result = []


def ready_data(path, table, table_type):
    if table == "sina":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        sina_data_count = 0
        sina_data = sql.queryall("select number, positive_number, negative_number, word_count, post_content_txt, order_pos, order_neg, order_nou from sina where "+ table_type +"_status = 0 and order_" + table_type + " is not null")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type))
        # 将数据写入txt文件
        count = 1
        for element in sina_data:
            sina_data_count += element.get('word_count')
            file_util.write_file(os.path.join(path, table, table + "_" + table_type, str(element.get(str('order_' + table_type))) + "-" + element.get('number') + ".txt"), element.get('post_content_txt'))
            count += 1
        finally_result.append(('sina ' + table_type + ' total word count', sina_data_count))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "sohu":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        sohu_data_count = 0
        sohu_data = sql.queryall("select number, positive_number, negative_number, word_count, article_content_txt, order_pos, order_neg, order_nou from sohu where "+ table_type + "_status = 0 and order_" + table_type + " is not null")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type))
        # 将数据写入txt文件
        count = 1
        for element in sohu_data:
            sohu_data_count += element.get('word_count')
            file_util.write_file(os.path.join(path, table, table + "_" + table_type, str(element.get('order_' + table_type)) + "-" + element.get('number') + ".txt"), element.get('article_content_txt'))
            count += 1
        finally_result.append(('sohu ' + table_type + ' total word count', sohu_data_count))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "tianya":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))
        tianya_word_count = 0
        tianya_data = sql.queryall("select number, positive_number, negative_number, word_count, question_detail, order_pos, order_neg, order_nou from tianya where "+ table_type +"_status = 0 and order_" + table_type + " is not null")

        # 清空文件夹并创建
        count = 1
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type))
        # 将数据写入txt文件
        for element in tianya_data:
            tianya_word_count += element.get('word_count')
            file_util.write_file(os.path.join(path, table, table + "_" + table_type, str(element.get('order_' + table_type)) + "-" + element.get('number') + ".txt"), element.get('question_detail'))
            count += 1
        finally_result.append(('tianya ' + table_type + ' total word count', tianya_word_count))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
        
def write_finally_txt(path):
    for element in finally_result:
        file_util.write_append_file(path, str(element))
        

def export_excel(path, tabel_name, table_type):
    result_data = sql.queryall("select number, positive_number, negative_number, word_count, order_pos, order_neg, order_nou from " + tabel_name + " where "+ table_type +"_status = 0 and order_" + table_type + " is not null order by order_" + table_type)
    xlwt_util.writeListData1(result_data, path, table_type)
    
        
if __name__ == '__main__':
    ready_data("/home/ftpUser/pub/finally", "sina", "pos")
    ready_data("/home/ftpUser/pub/finally", "sina", "neg")
    ready_data("/home/ftpUser/pub/finally", "sina", "nou")
    
    ready_data("/home/ftpUser/pub/finally", "sohu", "pos")
    ready_data("/home/ftpUser/pub/finally", "sohu", "neg")
    ready_data("/home/ftpUser/pub/finally", "sohu", "nou")
    
    ready_data("/home/ftpUser/pub/finally", "tianya", "pos")
    ready_data("/home/ftpUser/pub/finally", "tianya", "neg")
    ready_data("/home/ftpUser/pub/finally", "tianya", "nou")
    
    file_util.truncate_file(os.path.join('/home/ftpUser/pub/finally', 'finally.txt'))
    write_finally_txt(os.path.join('/home/ftpUser/pub/finally', 'finally.txt'))
    
    export_excel(os.path.join("/home/ftpUser/pub/finally", "sina", "sina_pos.csv"), "sina", "pos")
    export_excel(os.path.join("/home/ftpUser/pub/finally", "sina", "sina_neg.csv"), "sina", "neg")
    export_excel(os.path.join("/home/ftpUser/pub/finally", "sina", "sina_nou.csv"), "sina", "nou")
    
    export_excel(os.path.join("/home/ftpUser/pub/finally", "sohu", "sohu_pos.csv"), "sina", "pos")
    export_excel(os.path.join("/home/ftpUser/pub/finally", "sohu", "sohu_neg.csv"), "sina", "neg")
    export_excel(os.path.join("/home/ftpUser/pub/finally", "sohu", "sohu_nou.csv"), "sina", "nou")
    
    export_excel(os.path.join("/home/ftpUser/pub/finally", "tianya", "tianya_pos.csv"), "sina", "pos")
    export_excel(os.path.join("/home/ftpUser/pub/finally", "tianya", "tianya_neg.csv"), "sina", "neg")
    export_excel(os.path.join("/home/ftpUser/pub/finally", "tianya", "tianya_nou.csv"), "sina", "nou")