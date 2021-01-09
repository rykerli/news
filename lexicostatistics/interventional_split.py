# -*- encoding: utf-8 -*-
import jieba_fast as jieba
import codecs
import sys

sys.path.append("../utils")  # noqa
from file_util import *  # noqa

# 开启并行分词模式，参数为并行进程数
jieba.enable_parallel(4)


def split_word():
    with codecs.open(
        "../resource/vocabulary/intervention_word.txt", "r", encoding="utf8"
    ) as f1:
        data = f1.read()
    seg_list = jieba.cut(data, cut_all=False)
    list_str = " ".join(seg_list)

    with codecs.open("./split_intervention_word.txt", "w", encoding="utf8") as w:
        w.write(list_str)


if __name__ == "__main__":
    split_word()
