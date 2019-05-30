#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-23 16:52
@Author  : red
@Site    : 
@File    : import_word_excel.py
@Software: PyCharm
"""
from pyexcel_xls import get_data


def import_excel_data(path):
	xls_data = get_data(path)
	xls_data = xls_data['Sheet1']
	for element in xls_data:
		print(element)


if __name__ == '__main__':
	import_excel_data("/Users/red/Desktop/汉语态度系统表格.xlsx")
