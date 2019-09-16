#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/16 8:41 AM
@Author  : red
@Site    : 
@File    : cartesian.py
@Software: PyCharm
"""
import time

import itertools


class CartesianProduct(object):
    def __init__(self):
        self._data_list = []

    def add_data(self, data=None):  # 添加生成笛卡尔积的数据列表
        if data is None:
            data = []
        self._data_list.append(data)

    def build(self):  # 计算笛卡尔积
        return itertools.product(*self._data_list)
        # for item in itertools.product(*self._data_list):
        #     print("".join(item))
