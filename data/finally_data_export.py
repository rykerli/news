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


def ready_data(path, table, table_type):
    if table == "sina":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))

        sina_data = sql.queryall("select number, post_content_txt from sina where "+ table_type +"_status = 0")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type))
        # 将数据写入txt文件
        for element in sina_data:
            file_util.write_file(os.path.join(path, table, table + "_" + table_type, element.get('number') + ".txt"), element.get('post_content_txt'))
        
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "sohu":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))

        sohu_data = sql.queryall("select number, article_content_txt from sohu where "+ table_type +"_status = 0")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type))
        # 将数据写入txt文件
        for element in sohu_data:
            file_util.write_file(os.path.join(path, table, table + "_" + table_type, element.get('number') + ".txt"), element.get('article_content_txt'))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
    if table == "tianya":
        print("[{}]--write {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                                   table, table_type))

        tianya_data = sql.queryall("select number, question_detail from tianya where "+ table_type +"_status = 0")

        # 清空文件夹并创建
        dir_util.remove_dir(os.path.join(path, table, table + "_" + table_type))
        # 将数据写入txt文件
        for element in tianya_data:
            file_util.write_file(os.path.join(path, table, table + "_" + table_type, element.get('number') + ".txt"), element.get('question_detail'))
        print("[{}]--write {}_{} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), table, table_type))
        
        

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