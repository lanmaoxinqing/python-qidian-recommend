# -*- coding: utf-8 -*-
# !/usr/bin/python3

import urllib.parse as up
from pyquery import PyQuery as pq
try:
    from .model import *
except:
    from model import *


def parse():
    db.create_tables([FreeRank])
    path = 'http://www.jjwxc.net/topten.php?orderstr=1&timeid='
    page = 41
    # 页
    for i in range(1, page + 1):
        url = path + str(i)
        host = up.urlparse(url).hostname
        print(url)
        # 榜单列表
        # print(pq(url))
        # rank_arr = pq(url)("li")
        data = pq(url, encoding='gb2312')
        tables = data("table").filter(lambda i, this: pq(this).attr('cellpadding') == '3').items()

        for table in tables:
            book_ele = table('tr').eq(0)('td').eq(0)('a')
            id = book_ele.attr('href').split('=')[1]
            rank = FreeRank()
            rank.book_name = book_ele.text()
            rank.book_url = host + '/' + book_ele.attr('href')
            rank.id = id
            author_ele = table('tr').eq(0)('td').eq(1)('a')
            rank.author_name = author_ele.text()
            rank.author_url = host + '/' + author_ele.attr('href')
            rank.category = table('tr').eq(0)('td').eq(2).text()
            rank.tag = table('tr').eq(0)('td').eq(3).text()
            rank.state = table('tr').eq(0)('td').eq(4).text()
            rank.recommend_reason = table('.read_small').text()
            try:
                rank.save(force_insert=True)
            except:
                rank.save()

