# -*- coding: utf-8 -*-
# !/usr/bin/python3

from pyquery import PyQuery as pq
import aiohttp

try:
    from .model import *
except:
    from model import *



def parse():
    
    db.create_tables([FreeRank])
    path = 'http://www.jjwxc.net/topten.php?orderstr=1&timeid='
    page = 41

    loop = asyncio.get_event_loop()
    for i in range(1, page + 1):
        url = path + str(i)
        loop.run_until_complete(parse_detail(url))
    loop.close()

async def parse_detail(url):
    print(url)
    with (await sem):
        async with aiohttp.request('GET', url) as response:
            response = await response.text(encoding='gb2312', errors='ignore')
            data = pq(response)
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

                await update_detail(rank)


async def update_detail(rank):
    url = rank.book_url
    print(url)
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

