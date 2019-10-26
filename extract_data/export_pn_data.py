#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/9/16 4:50 PM
@Author  : red
@Site    : 
@File    : export_pn_data.py
@Software: PyCharm
"""
import sys

sys.path.append('../utils')
import time
import file_util as file
import sql_util as sql
import dir_util
import xlwt_util
import threading
import os


# 导出源语篇
class Thread(threading.Thread):
    def __init__(self, num, lst, path, category):
        self._path = path
        self._num = num
        self._lst = lst
        self._category = category
        super().__init__()

    def run(self):
        print("[{}]--write {} file start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._path, self._num, len(self._lst)))

        for element in self._lst:
            if self._category == 'sina':
                file.write_file(os.path.join(self._path, str(element.get('number')) + '.txt'),
                                element.get('post_content_txt'))
            elif self._category == 'sohu':
                file.write_file(os.path.join(self._path, str(element.get('number')) + '.txt'),
                                element.get('article_content_txt'))
            else:
                file.write_file(os.path.join(self._path, str(element.get('number')) + '.txt'),
                                element.get('question_detail'))
        print("[{}]--write {} file end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._path))


def start(path, data, category, step=1000):
    temp_list = [data[i:i + step] for i in range(0, len(data), step)]
    thr_list = [Thread(i, temp_list[i], path, category) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


def start_export_origin_main(sina, sohu, tianya):
    start(str(os.path.join(path, 'sina')), sina, 'sina', 5000)
    start(str(os.path.join(path, 'sohu')), sohu, 'sohu', 5000)
    start(str(os.path.join(path, 'tianya')), tianya, 'tianya', 5000)


# 导出统计积极消极词汇数量信息数据
def write_file(f_path, word_dict_data):
    for element in word_dict_data:
        # print(type(element))
        if element[1] != 0:
            file.write_append_file(f_path, str(element))


class Thread1(threading.Thread):
    def __init__(self, num, lst, path, category):
        self._path = path
        self._num = num
        self._lst = lst
        self._category = category
        super().__init__()

    def run(self):
        print("[{}]--write {} file start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._path, self._num, len(self._lst)))

        for element in self._lst:
            if self._category == 'sina':
                write_file(os.path.join(self._path, str(element.get('number')) + '.txt'),
                           eval(element.get('pn_word_count')))
            elif self._category == 'sohu':
                write_file(os.path.join(self._path, str(element.get('number')) + '.txt'),
                           eval(element.get('pn_word_count')))
            else:
                write_file(os.path.join(self._path, str(element.get('number')) + '.txt'),
                           eval(element.get('pn_word_count')))
        print("[{}]--write {} file end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._path))


def start1(path, data, category, step=1000):
    temp_list = [data[i:i + step] for i in range(0, len(data), step)]
    thr_list = [Thread1(i, temp_list[i], path, category) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


def start_export_count_main(sina, sohu, tianya):
    start1(str(os.path.join(path, 'sina_result')), sina, 'sina', 5000)
    start1(str(os.path.join(path, 'sohu_result')), sohu, 'sohu', 5000)
    start1(str(os.path.join(path, 'tianya_result')), tianya, 'tianya', 5000)


# 导出按照积极消极词数量排序后总结果
def get_sort_data():
    print("[{}]--start get sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_positive_data = sql.queryall(
        "select number, word_count, positive_number, negative_number from sina order by positive_number DESC")
    sina_negative_data = sql.queryall(
        "select number, word_count, positive_number, negative_number from sina order by negative_number DESC")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    print("[{}]--start get sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_positive_data = sql.queryall(
        "select number, word_count, positive_number, negative_number from sohu order by positive_number DESC")
    sohu_negative_data = sql.queryall(
        "select number, word_count, positive_number, negative_number from sohu order by negative_number DESC")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    print("[{}]--start get tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    tianya_positive_data = sql.queryall(
        "select number, word_count, positive_number, negative_number from tianya order by positive_number DESC")
    tianya_negative_data = sql.queryall(
        "select number, word_count, positive_number, negative_number from tianya order by negative_number DESC")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    return sina_positive_data, sina_negative_data, sohu_positive_data, sohu_negative_data, tianya_positive_data, tianya_negative_data


def write_sorted_data():
    path = '/home/ftpUser/pub/data/discourse_sort'
    dir_util.remove_dir("/home/ftpUser/pub/data/discourse_sort")

    sina_positive_data, sina_negative_data, sohu_positive_data, sohu_negative_data, tianya_positive_data, tianya_negative_data = get_sort_data()
    xlwt_util.writeListData(sina_positive_data,
                            os.path.join(path, 'sina_pos_sort.csv'))
    xlwt_util.writeListData(sina_negative_data,
                            os.path.join(path, 'sina_neg_sort.csv'))

    xlwt_util.writeListData(sohu_positive_data,
                            os.path.join(path, 'sohu_pos_sort.csv'))
    xlwt_util.writeListData(sohu_negative_data,
                            os.path.join(path, 'sohu_neg_sort.csv'))

    xlwt_util.writeListData(tianya_positive_data,
                            os.path.join(path, 'tianya_pos_sort.csv'))
    xlwt_util.writeListData(tianya_negative_data,
                            os.path.join(path, 'tianya_neg_sort.csv'))


# 获取数据结果
def get_data():
    print("[{}]--start get sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_data = sql.queryall("select * from sina")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    print("[{}]--start get sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_data = sql.queryall("select * from sohu")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    print("[{}]--start get tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    tianya_data = sql.queryall("select * from tianya")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    return sina_data, sohu_data, tianya_data


def start_main():
    path = "/home/ftpUser/pub/data"
    dir_util.remove_dir("/home/ftpUser/pub/data")
    dir_util.mkdir([os.path.join(path, 'sina'), os.path.join(path, 'sohu'), os.path.join(path, 'tianya')])
    dir_util.mkdir(
        [os.path.join(path, 'sina_result'), os.path.join(path, 'sohu_result'), os.path.join(path, 'tianya_result')])
    dir_util.mkdir('/home/ftpUser/pub/data/discourse_sort')
    # 获取数据
    sina, sohu, tianya = get_data()
    # 导出源语篇
    start_export_origin_main(sina, sohu, tianya)
    # 导出统计积极消极词汇数量信息数据
    start_export_count_main(sina, sohu, tianya)

    write_sorted_data()


if __name__ == '__main__':
    start()
