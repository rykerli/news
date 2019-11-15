#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2018-12-22 17:16
@Author  : red
@Site    : 
@File    : excel_util.py
@Software: PyCharm
"""

from pyexcel_xls import get_data
import os
import sql_util
import csv
import uuid


def read_csv_file(path):
    arrays = []
    with open(path, encoding='utf8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            row.insert(0, str(uuid.uuid4()))
            arrays.append(row)
    return arrays


def read_excel_data(path):
    return get_data(path)


def read_xls_file(path):
    arrays = []
    xls_data = get_data(path)
    for sheet_n in xls_data.keys():
        if (xls_data[sheet_n][0] == ['\ufeff"标题"', '时间', '正文', '阅读数', '网友', '评论', '评论时间', '点赞数']) or (
                xls_data[sheet_n][0] == ['标题', '时间', '正文', '阅读数', '网友', '评论', '评论时间', '点赞数']) or (
                xls_data[sheet_n][0] == ['标题', '时间', '正文', '字段2', '网友', '评论', '评论时间', '点赞数']) or (
                xls_data[sheet_n][0] == ['标题', '时间', '字段1', '字段2', '字段3', '字段4', '时间1', '字段5_文本']):
            temp = xls_data[sheet_n][1:]
            i = 1
            for item1 in temp:
                array1 = []
                array1.append(str(uuid.uuid4()))
                num = 0
                i += 1
                if len(item1) < 8:
                    num = 8 - len(item1)
                    # print("文件%s第%s行有%s个单元格为空" % (path, i, num))
                for item2 in item1:
                    array1.append(str(item2))
                for null in range(num):
                    array1.append("")
                arrays.append(array1)
        elif (xls_data[sheet_n][0] == ['标题', '时间', '类型', '正文', '阅读数', '网友', '评论', '评论时间', '点赞数']) or (
                xls_data[sheet_n][0] == ['title', 'ime', 'class', 'aricle', 'read', 'wangyou', 'review', 'reviewtime',
                                         'dianzan']):
            temp = xls_data[sheet_n][1:]
            i = 1
            for item1 in temp:
                array1 = []
                array1.append(str(uuid.uuid4()))
                num = 0
                i += 1
                if len(item1) < 9:
                    num = 9 - len(item1)
                    # print("文件%s第%s行有%s个单元格为空" % (path, i, num))
                for item2 in range(len(item1)):
                    if item2 != 2:
                        array1.append(item1[item2])
                for null in range(num):
                    array1.append("")
                arrays.append(array1)
        elif xls_data[sheet_n][0] == ['标题', '时间', '正文', '字段2', '网友', '评论', '评论时间', '点赞数', '阅读数']:
            temp = xls_data[sheet_n][1:]
            i = 1
            for item1 in temp:
                array1 = []
                array1.append(str(uuid.uuid4()))
                num = 0
                i += 1
                if len(item1) < 9:
                    num = 9 - len(item1)
                    # print("文件%s第%s行有%s个单元格为空" % (path, i, num))
                for item2 in range(len(item1)):
                    if item2 != 3:
                        array1.append(item1[item2])
                for null in range(num):
                    array1.append("")
                arrays.append(array1)
        elif xls_data[sheet_n][0] == ['标题', '时间', '正文', '网友', '评论', '点赞数']:
            temp = xls_data[sheet_n][1:]
            i = 1
            for item1 in temp:
                array1 = []
                array1.append(str(uuid.uuid4()))
                num = 0
                i += 1
                if len(item1) < 6:
                    num = 6 - len(item1)
                    # print("文件%s第%s行有%s个单元格为空" % (path, i, num))
                for item2 in range(len(item1)):
                    array1.append(item1[item2])
                for null in range(num + 2):
                    array1.append("")
                arrays.append(array1)
        elif xls_data[sheet_n][0] == ['标题', '时间', '字段1', '字段2']:
            temp = xls_data[sheet_n][1:]
            i = 1
            for item1 in temp:
                array1 = []
                array1.append(str(uuid.uuid4()))
                num = 0
                i += 1
                if len(item1) < 4:
                    num = 6 - len(item1)
                    # print("文件%s第%s行有%s个单元格为空" % (path, i, num))
                for item2 in range(len(item1) - 1):
                    array1.append(item1[item2])
                for null in range(num + 5):
                    array1.append("")
                arrays.append(array1)
    return arrays


def get_file_list(dir_path, file_list):
    if os.path.isfile(dir_path):
        file_list.append(dir_path)
    elif os.path.isdir(dir_path):
        for s in os.listdir(dir_path):
            new_dir = os.path.join(dir_path, s)
            get_file_list(new_dir, file_list)
    return file_list


if __name__ == '__main__':
    sql = "truncate table origin_data"
    sql_util.execute(sql)

    sql_str = "insert into origin_data(id, title, time, content, read_num, user, comment, comment_time, like_num) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    file_list = get_file_list("/Users/red/Desktop/temp/news/data", [])
    for file_path in file_list:
        suffix = str.split(file_path, ".")
        if suffix[-1] == "xlsx" or suffix[-1] == "xls":
            print("处理excel文件%s" % file_path)
            arrays = read_xls_file(file_path)
            result = sql_util.insertmany(sql_str, arrays)
            print("插入数据%s条" % result)
        elif suffix[-1] == "csv":
            print("处理csv文件%s" % file_path)
            arrays = read_csv_file(file_path)
            result = sql_util.insertmany(sql_str, arrays)
            print("插入数据%s条" % result)
