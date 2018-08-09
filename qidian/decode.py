# !/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
from fontTools.ttLib import TTFont

en_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0',
    'period': '.',
}


def decode(font_url, secret_str):
    path = 'Font/' + os.path.basename(font_url)
    if not os.path.exists('Font'):
        os.makedirs('Font')
    if not os.path.exists(path):
        download(font_url, path)
    font = TTFont(path)
    # font.saveXML('font.xml')
    font_map = font.getBestCmap()
    # print(font_map)
    result_str = ''
    for i in range(len(secret_str)):
        # print(secret_str[i])
        key = ord(secret_str[i])
        en = font_map[key]
        num = en_map[en]
        result_str += num
        # print(num)
    return float(result_str)


def download(url, path):
    r = requests.get(url).content
    with open(path, 'wb') as file:
        file.write(r)


def test():
    url = 'https://qidian.gtimg.com/qd_anti_spider/MZYjnXxB.ttf'
    str1 = '&#100101;&#100097;&#100097;&#100090;&#100094;&#100099;'
    result = '200.86'


    url2 = 'https://qidian.gtimg.com/qd_anti_spider/rtvNQrmI.ttf'
    str2 = '&#100378;&#100382;&#100376;&#100374;&#100376;&#100375;'
    result2 = '206.69'


    decode(url, str1)
    decode(url2, str2)

# test()