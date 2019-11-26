#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Time    : 2019/11/26 10:37 AM
@Author  : red
@Site    : 
@File    : test2.py
@Software: PyCharm
"""
import time
import math
from PIL import Image
import sys
import os


def cut_image(image, cut_num):
    """
    切图 1928*1024
    :param image:
    :return:
    """
    flag_value = int(math.sqrt(cut_num))
    width, height = image.size
    item_width = int(width / flag_value)
    print(item_width)
    item_height = int(height / flag_value)
    print(item_height)
    box_list = []
    for i in range(0, flag_value):
        for j in range(0, flag_value):
            box = (j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]

    return image_list


# def fill_image(image):
#     """
#     将图片填充为正方形
#     :param image:
#     :return:
#     """
#     width, height = image.size
#     #选取长和宽中较大值作为新图片的
#     new_image_length = width if width > height else height
#     #生成新图片[白底]
#     new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
#     #将之前的图粘贴在新图上，居中
#     if width > height:#原图宽大于高，则填充图片的竖直维度
#         #(x,y)二元组表示粘贴上图相对下图的起始位置
#         new_image.paste(image, (0, int((new_image_length - height) / 2)))
#     else:
#         new_image.paste(image,(int((new_image_length - width) / 2),0))

#     return new_image


def save_images(image_list):
    """
    保存
    :param image_list:
    :return:
    """
    index = 1
    dirs = './img_add/'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    for image in image_list:
        image.save(dirs + str(index) + '.png', 'PNG')
        index += 1


def main(file_path, batch_size):
    image = Image.open(file_path)
    # image = fill_image(image)
    image_list = cut_image(image, batch_size)
    save_images(image_list)


if __name__ == '__main__':
    batch_size = 64
    file_path = "train.png"  # 图片路径
    main(file_path, batch_size)
