#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-05-23 16:31
@Author  : red
@Site    : 
@File    : import_word_docx.py
@Software: PyCharm
"""
import docx
from docx import Document


def import_docx(path):
	document = Document(path)
	tables = document.tables  # 获取文件中的表格集
	table = tables[0]  # 获取文件中的第一个表格
	for i in range(0, len(table.rows)):  # 从表格第二行开始循环读取表格数据
		result = table.cell(i, 0).text + " " + table.cell(i, 1).text + table.cell(i, 2).text + table.cell(i,
																										  3).text + table.cell(
			i, 4).text
		# cell(i,0)表示第(i+1)行第1列数据，以此类推
		print(result)


if __name__ == '__main__':
	import_docx("/Users/red/Desktop/汉语态度系统表格.docx")
