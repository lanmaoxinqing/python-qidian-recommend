# -*- coding: utf-8 -*-
# !/usr/bin/python3

# from pyquery.ajax import PyQuery as pqajax
from pyquery import PyQuery as pq
from model import *
import os


def parse():
    path = "https://www.qidian.com/book/strongrec?page="
    page = 10
    # 页
    for i in range(1, page + 1):
        url = path + str(i)
        print(url)
        # 榜单列表
        # print(pq(url))
        # rank_arr = pq(url)("li")
        data = pq(url)
        rank_arr = data("li")(".strongrec-list").items()
        # 减掉 < 和 >
        page = data(".lbf-pagination-item").size() - 2
        # print(rank_arr)
        # 榜单
        for rank_data in rank_arr:
            rank = Rank()
            rank.type = 1
            rank.fromDate = rank_data(".date-from").text()
            rank.toDate = rank_data(".date-to").text()
            rank.save()
            # print(rank.fromDate, rank.toDate)
            # 小说列表
            book_arr = rank_data(".book-list")("li").items()
            for book_data in book_arr:
                channel_data = book_data(".channel")
                channel = Channel()
                channel.url = channel_data.attr("href")
                channel.id = os.path.basename(channel.url)
                channel_data("em").remove()
                channel.name = channel_data.text()
                channel.save()

                author_data = book_data(".author")
                author = Author()
                author.name = author_data.text()
                author.url = author_data.attr("href")
                author.id = author.url.split("=")[1]
                author.save()

                book_data = book_data(".name")
                book = Book()
                book.name = book_data.text()
                book.url = book_data.attr("href")
                book.id = os.path.basename(book.url)
                book.channel = channel
                book.author = author
                # print(book.channel, book.name, book.author)
                book.save()

                rank_book = RankBook()
                rank_book.rank = rank
                rank_book.book = book
                rank_book.bookName = book.name
                rank_book.bookURL = book.url
                rank_book.authorName = author.name
                rank_book.channelName = channel.name
                rank_book.save()


db.connect()
db.create_tables([RankBook, Book, Rank, Author, Channel])
parse()
db.close()
