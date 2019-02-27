#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-26 07:58
@Author  : red
@Site    : 
@File    : file_util.py
@Software: PyCharm
"""


def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf8') as w:
        w.write(content)
