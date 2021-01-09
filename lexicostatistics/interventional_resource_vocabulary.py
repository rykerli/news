# -*- encoding: utf-8 -*-
import os
import sys
import re

sys.path.append("../utils")  # noqa
import sql_util as sql  # noqa
from xlwt_util import *  # noqa

"""
介入资源词汇统计
"""


def get_data():
    sina_data = sql.queryall(
        "select number, pos_status, neg_status, remove_useless, post_content_txt "
        "from sina where pos_status=0 or neg_status = 0"
    )
    sohu_data = sql.queryall(
        "select number, negative_number, pos_status, neg_status, remove_useless, article_content_txt "
        "from sohu where pos_status = 0 or neg_status = 0"
    )
    tianya_data = sql.queryall(
        "select number, negative_number, pos_status, neg_status, remove_useless, question_detail "
        "from tianya where pos_status = 0 or neg_status = 0"
    )
    return {"sina": sina_data, "sohu": sohu_data, "tianya": tianya_data}


def get_txt_data():
    with open("../resource/vocabulary/intervention_word.txt", "r") as f:
        txt_data = f.read()
    result = [item for item in txt_data.split("\n")]
    return result


def count_word(data, intervention_word):
    """
    词汇统计
    :parm data
    :return:
    """
    all_data = {}
    result = []
    intervention_word_copy = intervention_word[:]
    for sina in data["sina"]:
        sina_data = [sina["number"], sina["post_content_txt"]]
        intervention_word_result = []
        re_result = []
        for i, word in enumerate(intervention_word_copy):
            if "......" in word:
                re_data = re.findall(
                    word.replace("......", r"\w.{1,5}?"), sina["remove_useless"]
                )
            else:
                re_data = re.findall(word, sina["remove_useless"])
            if re_data:
                re_result.extend(re_data)
                intervention_word_result.append(intervention_word[i])
        write_html_file(sina["number"], sina["post_content_txt"], re_result, "sina")
        sina_data.extend(
            [
                ",".join(list(set(intervention_word_result))),
                len(list(set(intervention_word_result))),
                len(intervention_word_result),
                get_status(sina["pos_status"], sina["neg_status"]),
                "sina/{}.html".format(sina["number"]),
            ]
        )
        result.append(sina_data)
    all_data.update({"sina": result})
    result = []
    intervention_word_copy = intervention_word[:]
    for sohu in data["sohu"]:
        sohu_data = [sohu["number"], sohu["article_content_txt"]]
        intervention_word_result = []
        re_result = []
        for i, word in enumerate(intervention_word_copy):
            if "......" in word:
                re_data = re.findall(
                    word.replace("......", r"\w.{1,5}?"), sohu["remove_useless"]
                )
            else:
                re_data = re.findall(word, sohu["remove_useless"])
            if re_data:
                re_result.extend(re_data)
                intervention_word_result.append(intervention_word[i])
        write_html_file(sohu["number"], sohu["article_content_txt"], re_result, "sohu")
        sohu_data.extend(
            [
                ",".join(list(set(intervention_word_result))),
                len(list(set(intervention_word_result))),
                len(intervention_word_result),
                get_status(sohu["pos_status"], sohu["neg_status"]),
                "sohu/{}.html".format(sohu["number"]),
            ]
        )
        result.append(sohu_data)
    all_data.update({"sohu": result})
    result = []
    intervention_word_copy = intervention_word[:]
    for tianya in data["tianya"]:
        tianya_data = [tianya["number"], tianya["question_detail"]]
        intervention_word_result = []
        re_result = []
        for i, word in enumerate(intervention_word_copy):
            if "......" in word:
                re_data = re.findall(
                    word.replace("......", r"\w.{1,5}?"), tianya["remove_useless"]
                )
            else:
                re_data = re.findall(word, tianya["remove_useless"])
            if re_data:
                re_result.extend(re_data)
                intervention_word_result.append(intervention_word[i])
        write_html_file(
            tianya["number"], tianya["question_detail"], re_result, "tianya"
        )
        tianya_data.extend(
            [
                ",".join(list(set(intervention_word_result))),
                len(list(set(intervention_word_result))),
                len(intervention_word_result),
                get_status(tianya["pos_status"], tianya["neg_status"]),
                "tianya/{}.html".format(tianya["number"]),
            ]
        )
        result.append(tianya_data)
    all_data.update({"tianya": result})
    return all_data


def get_status(pos_status, neg_status):
    if not pos_status:
        return "积极"
    if not neg_status:
        return "消极"


def write_html_file(number, text, replace_color_text_list, type):
    for replace_color_text in list(set(replace_color_text_list)):
        text = text.replace(
            replace_color_text, "<span>{}</span>".format(replace_color_text)
        )
    text = "<p>{}</p>".format(text)

    html_text = (
        """
            <!DOCTYPE HTML>
                <html>
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <title>文件预览</title>
                <style type="text/css">
                span{
                   color:red;
                }
                </style>
                </head>
                <body>
                    %s
                </body>
                </html>
            """
        % text
    )
    with open(
        os.path.join("../resource/data/html_file/" + type + "/", number + ".html"), "w"
    ) as w:
        w.write(html_text)


def write_data_excel(data):
    sina_data = data["sina"]
    book_name_xls = "../resource/data/新浪介入词统计.xls"
    write_excel_xls(  # noqa
        book_name_xls,
        "新浪介入词统计",
        [["编号", "文本", "介入词", "介入词数量", "介入词出现次数", "类型", "预览地址"]],
    )
    write_excel_xls_append(book_name_xls, sina_data)  # noqa

    sohu_data = data["sohu"]
    book_name_xls = "../resource/data/搜狐介入词统计.xls"
    write_excel_xls(  # noqa
        book_name_xls,
        "搜狐介入词统计",
        [["编号", "文本", "介入词", "介入词数量", "介入词出现次数", "类型", "预览地址"]],
    )
    write_excel_xls_append(book_name_xls, sohu_data)  # noqa

    tianya_data = data["tianya"]
    book_name_xls = "../resource/data/天涯介入词统计.xls"
    write_excel_xls(  # noqa
        book_name_xls,
        "天涯介入词统计",
        [["编号", "文本", "介入词", "介入词数量", "介入词出现次数", "类型", "预览地址"]],
    )
    write_excel_xls_append(book_name_xls, tianya_data)  # noqa


if __name__ == "__main__":
    result = count_word(get_data(), get_txt_data())
    write_data_excel(result)
