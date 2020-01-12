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
    # 根据传入的number查到本条记录并取得pn_word_count，再根据pn_word_count和pos_status=0查询是否已经存在相同的文章
    print("[{}]--update {}_{} data  start......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                        table, table_type))
    faild = []
    arrays = excel.read_excel_data(path)

    #     result = []
    for sheet_n in arrays.keys():
        if arrays[sheet_n]:
            count = 0
            for item in arrays[sheet_n][1:]:
                pn_word_count = sql.queryone('select pn_word_count from ' + table + ' where number = %s',
                                             str('0' * (8 - len(str(item[0]))) + str(item[0])))
                tmp_result = sql.queryall(
                    'select * from ' + table + ' where pn_word_count = %s and ' + table_type + '_status = 0',
                    pn_word_count)
                if not tmp_result:
                    count += 1
                    sql.execute(
                        'update ' + table + ' set ' + table_type + '_status = %s, order_' + table_type + ' = %s where number = %s ',
                        (int(0), int(count), str('0' * (8 - len(str(item[0]))) + str(item[0]))))


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
