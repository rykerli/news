# -*- encoding: utf-8 -*-
import xlwt
import csv

from xlutils.copy import copy
import xlrd

"""
title = ['','','']
array = [['','',''], ['','',''], ['','','']...]
"""


def writeListData(data, name):
    temp = [("file name", "positive number", "negative number", "word count")]
    for element in data:
        temp.append(
            (
                element.get("number"),
                element.get("positive_number"),
                element.get("negative_number"),
                element.get("word_count"),
            )
        )
    with open(name, "a", errors="ignore", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(temp)
    # print('write_csv success')


def writeListData1(data, name, table_type):
    temp = [
        (
            "file name",
            "positive number",
            "negative number",
            "word count",
            str("order " + table_type),
        )
    ]
    for element in data:
        temp.append(
            (
                element.get("number"),
                element.get("positive_number"),
                element.get("negative_number"),
                element.get("word_count"),
                element.get("order_" + table_type),
            )
        )
    with open(name, "a", errors="ignore", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(temp)
    # print('write_csv success')


def writeData(data, name):
    temp = []
    for element in data:
        if element.get("") != 0:
            temp.append(element)
    with open(name, "a", errors="ignore", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(temp)


def save_xlwt(col_num, sheet_name, title, array, save_path):
    excel_table = xlwt.Workbook()
    sheet1 = excel_table.add_sheet(sheet_name, cell_overwrite_ok=True)
    for i in range(col_num):
        sheet1.write(0, i, title[i])
    for i in range(len(array)):
        for j in range(col_num):
            sheet1.write(i + 1, j, array[i][j])
    excel_table.save(save_path)


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(
                i + rows_old, j, value[i][j]
            )  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


if __name__ == "__main__":
    book_name_xls = "xls格式测试工作簿.xls"

    sheet_name_xls = "xls格式测试表"

    value_title = [
        ["姓名", "性别", "年龄", "城市", "职业"],
    ]

    value1 = [
        ["张三", "男", "19", "杭州", "研发工程师"],
        ["李四", "男", "22", "北京", "医生"],
        ["王五", "女", "33", "珠海", "出租车司机"],
    ]

    value2 = [
        ["Tom", "男", "21", "西安", "测试工程师"],
        ["Jones", "女", "34", "上海", "产品经理"],
        ["Cat", "女", "56", "上海", "教师"],
    ]

    # writeData([(1, 1), (2, 3)], "./tmp.csv")
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    write_excel_xls_append(book_name_xls, value1)
    write_excel_xls_append(book_name_xls, value2)
