# !/usr/bin/python3
# -*- coding: utf-8 -*-

import parser
from pyquery import PyQuery as pq
from qidian.model import *
import os
import qidian.decode as qd
import html

'''
    全本列表
'''


class FinishParser(parser.Parser):

    def start(self, url, mode, encode):
        db.create_tables([FinishBook])
        super().start(url, mode, encode)

    def parse_page_list(self):
        path = 'https://www.qidian.com/finish' \
               '?action=hidden' \
               '&orderId=' \
               '&style=1' \
               '&pageSize=20' \
               '&siteid=1' \
               '&pubflag=0' \
               '&hiddenField=0' \
               '&page='
        urls = []
        count = len(FinishBook.select(FinishBook.book_id))
        current_page = int(count / 20) + 1
        total = 49271
        for i in range(current_page, total):
            url = path + str(i)
            urls.append(url)
        return urls

    def parse_page(self, response):
        # print(response)
        book_eles = pq(response)('.all-img-list')('li').items()
        with db.atomic():
            for book_ele in book_eles:
                book = FinishBook()
                book.cover_url = 'http:' + book_ele('img').attr('src')
                book.book_id = book_ele('.book-mid-info').children('h4')('a').attr('data-bid')
                book.book_name = book_ele('.book-mid-info').children('h4')('a').text()
                book.book_url = 'https:' + book_ele('.book-mid-info').children('h4')('a').attr('href')
                book.author_id = os.path.basename(book_ele('.author')('.name').attr('href'))
                book.author_name = book_ele('.author')('.name').text()
                book.category = book_ele('.author')('a').eq(1).text()
                book.sub_category = book_ele('.author')('.go-sub-type').text()
                book.state = book_ele('.author')('span').text()
                book.desc = book_ele('.intro').text()
                secret_key = book_ele('.update')('span').children()('span').attr('class')
                if secret_key:
                    # print(book.desc, book.book_name, secret_key)
                    font_url = 'https://qidian.gtimg.com/qd_anti_spider/' + secret_key + '.ttf'
                    word_str = book_ele('.update')('.' + secret_key).text()
                    book.word_count = qd.decode(font_url, word_str) * 10000
                # print(book.word_count, book.book_name)
                try:
                    book.save(force_insert=True)
                except:
                    book.save()
