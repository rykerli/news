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
import sys
sys.path.append('../utils')
import sql_util as sql
import xlwt_util
import excel_util as excel


def read_data(path, table, table_type):
    print("[{}]--update {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                               table, table_type))
    faild = []
    arrays = excel.read_excel_data(path)
    count = 0
    for sheet_n in arrays.keys():
        if arrays[sheet_n]:
            for item in arrays[sheet_n][1:]:
                count+=1
                # 更新数据
                temp = sql.execute("update " + table + " set " + table_type + "_status = %s where number = %s", (int(0), '0' * (8 - len(str(item[0]))) + str(item[0])))
                if temp == 0:
                    faild.append('0' * (8 - len(str(item[0]))) + str(item[0]))
    print("[{}]--update count {} data  end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                               count))
    print("faild list: {}", faild)

if __name__ == '__main__':
    read_data("/home/data/news/dataupdate/sina-pos.xlsx", "sina", "pos")
    read_data("/home/data/news/dataupdate/sina-neg.xlsx", "sina", "neg")
    read_data("/home/data/news/dataupdate/sina-neu.xlsx", "sina", "nou")
    
    read_data("/home/data/news/dataupdate/soho_pos.xlsx", "sohu", "pos")
    read_data("/home/data/news/dataupdate/soho-neg.xlsx", "sohu", "neg")
    read_data("/home/data/news/dataupdate/soho_neu.xlsx", "sohu", "nou")
    
    read_data("/home/data/news/dataupdate/Tianya-pos2019.11.10.xlsx", "tianya", "pos")
    read_data("/home/data/news/dataupdate/Tianya-neg2019.11.10.xlsx", "tianya", "neg")
    read_data("/home/data/news/dataupdate/Tianya-neu2019.11.10.xlsx", "tianya", "nou")
