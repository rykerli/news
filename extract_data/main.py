#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/23 7:32 PM
@Author  : red
@Site    : 
@File    : main.py
@Software: PyCharm
"""
import sys
# sys.path.append('../export')
# sys.path.append('../file_process')
import time
# from export import export_data_txt_one
# import write_file, rename_file
# import count_word, txt_sort

if __name__ == '__main__':
    """
    按要求(字数大于80小于1800的语篇)将原始数据加工处理得到大数据库，初始数据不动，添加字数统计、编号字段，合并两个搜狐库
    parm1:数据取多少条，0代表全部数据
    parm2:语篇最小字数
    parm3:语篇最大字数
    """
    extract_origin_data.main(0, 80, 1800)
    """
    统计语篇的积极词汇和消极词汇，并计算词频
    """
    count_word_sql.start_main()
    