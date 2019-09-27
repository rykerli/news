#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019-02-26 07:58
@Author  : red
@Site    : 
@File    : file_util.py
@Software: PyCharm
"""
import math
import os


def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf8') as w:
        w.write(content)


def append_file(file_path, content):
    with open(file_path, 'a', encoding='utf8') as w:
        w.write(content)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf8') as r:
        rs = r.readlines()
    return rs


# 判断输入的路径是文件还是文件夹、或是否存在
def check_file(path):
    if not path:
        return False, -1
    import os
    if os.path.isfile(path):
        return True, 1
    elif os.path.isdir(path):
        return True, 0
    else:
        return False, -1


# 格式化花费时间
def formated_time(time):
    if time / 60 / 60 >= 1:
        hour = math.floor(time / 60 / 60)
        min = (time / 60 / 60 - hour) * 60
        if (min - int(min)) * 60 - math.floor((min - int(min)) * 60) > 0.5:
            sec = math.ceil((min - int(min)) * 60)
        else:
            sec = math.floor((min - int(min)) * 60)
        return '%dh:%dm:%ds' % (hour, min, sec)
    elif time / 60 >= 1:
        min = math.floor(time / 60)
        if (time / 60 - min) * 60 - math.floor((time / 60 - min) * 60) > 0.5:
            sec = math.ceil((time / 60 - min) * 60)
        else:
            sec = math.floor((time / 60 - min) * 60)
        return '%dm:%ds' % (min, sec)
    else:
        return '%.2fs' % time


# 格式化文件尺寸
def formated_size(size):
    if size / 1024 / 1024 / 1024 >= 1:
        show_size = size / 1024 / 1024 / 1024
        unit = 'Gb'
    elif size / 1024 / 1024 >= 1:
        show_size = size / 1024 / 1024
        unit = 'Mb'
    elif size / 1024 >= 1:
        show_size = size / 1024
        unit = 'Kb'
    else:
        show_size = size
        unit = 'b'
    return '%.2f' % show_size + unit


# 判断文件大小的单位
def judge_unit(size):
    if size / 1024 / 1024 / 1024 >= 1:
        show_size = size / 1024 / 1024 / 1024
        unit = 'Gb'
    elif size / 1024 / 1024 >= 1:
        show_size = size / 1024 / 1024
        unit = 'Mb'
    elif size / 1024 >= 1:
        show_size = size / 1024
        unit = 'Kb'
    else:
        show_size = size
        unit = 'b'
    return (show_size, unit)


# 获取相对路径
def relative_path(root, absolute_path):
    relative_path = str(absolute_path)[str(absolute_path).find(root) + len(root) + 1:]
    if not relative_path:
        relative_path = ''
    return relative_path


# 自适应Windows、macos、linux 路径分隔符
def dir_divider():
    import platform
    if platform.platform().find('Windows') != -1:
        return '\\'
    else:
        return '/'


# 自适应Windows、macos、linux 路径分隔符 相反
def anti_dir_divider():
    import platform
    if platform.platform().find('Windows') != -1:
        return '/'
    else:
        return '\\'


# 获取文件的md5值
def getFileMd5(filename):
    import os
    if not os.path.isfile(filename):
        return ''
    import hashlib
    myhash = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
    return myhash.hexdigest()


def write_append_file(file_path, content):
    with open(file_path, 'a') as w:
        w.write(content)
        w.write('\n')


def get_file_list(dir_path, file_list):
    # 如果是文件则添加进 fileList
    if os.path.isfile(dir_path):
        file_list.append(dir_path)
    elif os.path.isdir(dir_path):
        for s in os.listdir(dir_path):  # 如果是文件夹
            new_dir = os.path.join(dir_path, s)
            get_file_list(new_dir, file_list)
    return file_list


def get_file_list_end_with(dir_path, file_list, file_end_with=""):
    # 如果是文件则添加进 fileList
    if os.path.isfile(dir_path) & (os.path.splitext(dir_path)[-1][1:] == file_end_with):
        file_list.append(dir_path)
    elif os.path.isdir(dir_path):
        for s in os.listdir(dir_path):  # 如果是文件夹
            new_dir = os.path.join(dir_path, s)
            get_file_list_end_with(new_dir, file_list, file_end_with)
    return file_list


def truncate_file(file_path):
    result1, result2 = check_file(file_path)
    if result1:
        with open(file_path, "r+") as f:
            f.truncate()


if __name__ == '__main__':
    print(read_file('/Users/red/Desktop/temp/news/data/sj_data/all_data/article_txt.txt'))
