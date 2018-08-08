# -*- coding: utf-8 -*-
# !/usr/bin/python3

from pyquery import PyQuery as pq
import aiohttp
import asyncio

try:
    from .model import *
except:
    from model import *


host = 'http://www.jjwxc.net'
sem = asyncio.Semaphore(5)

def parse():
    db.create_tables([VipRank])
    urls = parse_list()
    loop = asyncio.get_event_loop()
    for url in urls:
        loop.run_until_complete(parse_content(url))
    loop.close()

def parse_list():
    path = 'http://www.jjwxc.net/topten.php?orderstr=2&timeid='
    data = pq(path, encoding='gb2312')('td').filter(lambda i, this: pq(this).attr('height') == '18')('a')
    urls = []
    for a in data.items():
        url = host + '/' + a.attr('href')
        urls.append(url)
    return urls


async def parse_content(url):
    print(url)
    with (await sem):
        async with aiohttp.request('GET', url) as response:
            response = await response.text(encoding='gb2312', errors='ignore')
            data = pq(response)
            tables = data("table").filter(lambda i, this: pq(this).attr('cellpadding') == '3').items()
            with db.atomic():
                for table in tables:
                    book_ele = table('tr').eq(0)('td').eq(0)('a')
                    id = book_ele.attr('href').split('=')[1]
                    rank = VipRank()
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

                    (word_count, collect_count) = await parse_detail(rank.book_url)
                    if word_count:
                        rank.word_count = word_count
                    if collect_count:
                        rank.collect_count = collect_count
                    print(rank.book_name, rank.word_count)
                    try:
                        rank.save(force_insert=True)
                    except:
                        rank.save()


async def parse_detail(url):
    async with aiohttp.request('GET', url) as response:
        response = await response.text(encoding='gb2312', errors='ignore')
        data = pq(response)
        word_count = data("span").filter(lambda i, this: pq(this).attr('itemprop') == 'wordCount').eq(0).text()
        collect_count = data("span").filter(lambda i, this: pq(this).attr('itemprop') == 'collectedCount').eq(0).text()
        return (word_count.rstrip('字'), collect_count)


def update():
    loop = asyncio.get_event_loop()
    ranks = VipRank.raw('select * from viprank where collect_count = 0 and book_url is not null')
    for rank in ranks:
        loop.run_until_complete(update_detail(rank))
    loop.close()


async def update_detail(rank):
    url = rank.book_url
    print(url)
    with (await sem):
        async with aiohttp.request('GET', url) as response:
            response = await response.text(encoding='gb2312', errors='ignore')
            data = pq(response)
            word_count = data("span").filter(lambda i, this: pq(this).attr('itemprop') == 'wordCount').eq(0).text()
            collect_count = data("span").filter(lambda i, this: pq(this).attr('itemprop') == 'collectedCount').eq(0).text()
            if word_count:
                rank.word_count = word_count.rstrip('字')
            if collect_count:
                rank.collect_count = collect_count
            rank.save()
