#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-26 20:12
@Author  : red
@Site    : 
@File    : xlwt_util.py
@Software: PyCharm
"""
import xlwt

"""
title = ['','','']
array = [['','',''], ['','',''], ['','','']...]
"""


def save_xlwt(col_num, sheet_name, title, array, save_path):
    excel_table = xlwt.Workbook()
    sheet1 = excel_table.add_sheet(sheet_name, cell_overwrite_ok=True)
    for i in range(col_num):
        sheet1.write(0, i, title[i])
    for i in range(len(array)):
        for j in range(col_num):
            sheet1.write(i + 1, j, array[i][j])
    excel_table.save(save_path)
