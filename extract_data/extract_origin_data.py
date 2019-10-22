#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/10/21 6:14 PM
@Author  : red
@Site    : 
@File    : extract_origin_data.py
@Software: PyCharm
"""
import time
import sys

sys.path.append('../utils')
import time
import sql_util as sql
import file_util
from operator import itemgetter
from itertools import groupby
import re
import time
import threading


def get_sina_data(limit, min_num, max_num):
    print("[{}]--start process sina sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sina_article = sql.queryall(
            "select * from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + str(max_num) + " limit " + str(
                limit))
    else:
        sina_article = sql.queryall(
            "select * from sj_sina where CHAR_LENGTH(TRIM(post_content_txt)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(post_content_txt)) < " + str(max_num) + "")
    print("[{}]--process sina sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def get_tianya_data(limit, min_num, max_num):
    print("[{}]--start process tianya sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        ty_article = sql.queryall(
            "select * from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + str(max_num) + " limit " + str(limit))
    else:
        ty_article = sql.queryall(
            "select * from sj_tianya where CHAR_LENGTH(TRIM(question_detail)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(question_detail)) < " + str(max_num) + "")
    print("[{}]--process tianya sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def get_sohu_data(limit, min_num, max_num):
    print("[{}]--start process sohu sql......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    if limit != 0:
        sohu_article = sql.queryall(
            "select * from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + str(min_num)
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + str(max_num) + " limit " + str(limit))
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_origin_data where CHAR_LENGTH(TRIM(content)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(content)) < " + str(max_num) + " limit " + str(limit))
    else:
        sohu_article = sql.queryall(
            "select * from sj_sohu where CHAR_LENGTH(TRIM(article_content)) > " + str(min_num)
            + "  and CHAR_LENGTH(TRIM(article_content)) < " + str(max_num) + "")
        bzy_sohu_article = sql.queryall(
            "select * from bzy_sohu_origin_data where CHAR_LENGTH(TRIM(content)) > " + str(min_num)
            + " and CHAR_LENGTH(TRIM(content)) < " + str(max_num) + "")
    print("[{}]--process sohu sql data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_article, bzy_sohu_article


def process_sina_data(limit, min_num, max_num):
    print("[{}]--start process data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sina_article = get_sina_data(limit, min_num, max_num)
    # sina_result = []
    #
    # for element in sina_article:
    #     temp = [str(element.get('id')), str(element.get('post_content_txt'))]
    #     sina_result.append(temp)
    print("[{}]--process data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sina_article


def process_tianya_data(limit, min_num, max_num):
    print("[{}]--start process tianya data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    ty_article = get_tianya_data(limit, min_num, max_num)
    # ty_result = []
    # for element in ty_article:
    #     temp = [str(element.get('id')), str(element.get('question_detail'))]
    #     ty_result.append(temp)

    print("[{}]--process tianya data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return ty_article


def process_sohu_data(limit, min_num, max_num):
    print("[{}]--start process sohu data......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    sohu_article, bzy_sohu_article = get_sohu_data(limit, min_num, max_num)
    start(sohu_article)
    sohu_result = []
    sohu_result += sj_sohu_result
    # 开始处理sohu bzy数据并合并到数组
    for element in bzy_sohu_article:
        print(element)
        break
    print("[{}]--process sohu data end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    return sohu_result


sj_sohu_result = []


class Thread(threading.Thread):
    def __init__(self, num, lst):
        self._num = num
        self._lst = lst
        super().__init__()

    def run(self):
        print("[{}]--process start, process {} thread, num is {}......".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), self._num, len(self._lst)))
        # 循环处理数据，去掉每一条数据中的article_content html标签
        # 正则表达式过滤标签<>...</> or <.../>
        # for element in self._lst:
        #     file_util.write_file(os.path.join(self._path, element[0] + '.txt'),
        #                          element[1])
        count = 0
        for element in self._lst:

            temp = re.compile(r'<[^>]*>', re.S)
            temp = temp.sub('', element.get('article_content'))
            temp = str.replace(temp, '\n', '').strip()
            element['article_content_txt'] = temp
            sj_sohu_result.append(element)
            count += 1
        print("[{}]--process end......".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def start(sohu_article, step=5000):
    temp_list = [sohu_article[i:i + step] for i in range(0, len(sohu_article), step)]
    thr_list = [Thread(i, temp_list[i]) for i in range(len(temp_list))]
    [thr.start() for thr in thr_list]
    [thr.join() for thr in thr_list]


def main(limit, min_num, max_num):
    return process_sina_data(limit, min_num, max_num), process_sohu_data(limit, min_num, max_num), process_tianya_data(
        limit, min_num, max_num)


if __name__ == '__main__':
#     {'id': '1', 'time': 1548389177, 'article_link': 'http://m.sohu.com/a/291336783_114911?_f=m-channel_8_feeds_3', 'article_title': '内地游客玩无人机撞大三巴牌坊 澳门：已将涉事人员带走调查', 'article_content': '参考消息网1月24日报道海外媒体称，1月23日晚一名男游客玩航拍期间，疑似无人机突然故障无信号，撞击澳门大三巴牌坊后“坠落”二层窗口，当地保安报警处理。 据《澳门日报》1月24日报道，23日晚8点半许，澳门警方接到报案信息，称大三巴牌坊发生航拍无人机毁损事件，警员到场向保安及涉事的23岁内地男游客了解情况。据称有人玩航拍期间，疑似无人机突然无信号并失去动力，“降落”到牌坊二层中央窗口，现场人指称航拍机曾与牌坊发生碰撞后坠落。事发后现场被封锁，消防人员亦到场戒备，随后将无人机取下。 澳门警方表示，涉事航拍无人机未向当地申请航拍准照，涉案游客被带走调查。 另据香港《明报》网站1月24日报道，澳门文化局24日再次派人员详细检查大三巴牌坊，包括现场检视、照片比对及使用3D扫描作数据分析等，经过严谨检查后，确认大三巴牌坊没有受损。 报道称，澳门方面未来会加强公众对文物建筑安全的保护意识，并呼吁市民及游客使用航拍机时，除需遵守相关规定外，更应确保文物建筑安全，若令建筑受损，需负刑事责任。                                声明：该文观点仅代表作者本人，搜狐号系信息发布平台，搜狐仅提供信息存储空间服务。', 'article_author': '参考消息', 'article_avatar': 'http://img.mp.sohu.com/upload/20180122/b91280cae1434c90aa7286b3ac77142f', 'views_count': 78971, 'article_publish_time': 1548375849, 'article_topics': '[]', 'article_thumbnails': '[]', 'article_category': '新闻'}


# {'title': '以色列总理视察军力部署：已准备好对加沙采取大规模行动', 'time': '2019-03-29 19:16', 'content': '原标题：以色列总理视察军力部署：已准备好对加沙采取大规模行动            新京报快讯（记者 刘壹昭）据美联社报道，3月28日，以色列总理办公室发布消息，称以色列总理内塔尼亚胡当天视察了以色列国防军在加沙地带边境的兵力部署情况，并表示已经做好对加沙地带进行大规模行动的准备。 内塔尼亚胡在视察后表示，以色列正在加强加沙地带周边的安全部署，近日他已下令增调兵力和器械，做好对加沙地带进行大规模行动的准备。  3月27日，以色列军人坐在近以色列与加沙边界的军车上。图源：美联社 内塔尼亚胡的声明发表在哈马斯政权与以色列进行新一轮交火后，而埃及作为中间调停者，则寄望于双方拓展停火协议。 以色列国防军28日发表声明说，以军已在以色列南部加强军力部署，以应对即将到来的巴勒斯坦“土地日”可能出现的“暴力活动”升级情况。 新京报记者 刘壹昭 编辑 白爽 校对 危卓返回搜狐，查看更多      责任编辑：', 'user': '', 'comment': ''}
    process_sohu_data(10, 80, 1800)
