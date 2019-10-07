#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/23 7:32 PM
@Author  : red
@Site    : 
@File    : 500data.py
@Software: PyCharm
"""
import sys
sys.path.append('../export')
sys.path.append('../file_process')
import time
# from export import export_data_txt_one
import write_file, rename_file
import count_word, txt_sort

if __name__ == '__main__':
    # 导出文件并写入本地 limit=0处理所有数据
    write_file.start_main(0)
    # 重命名文件
    rename_file.start()
    # 统计词语
    count_word.start_main()
    # 语篇排序
    txt_sort.start()
