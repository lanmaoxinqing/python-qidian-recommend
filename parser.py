# -*- coding: utf-8 -*-
# !/usr/bin/python3

import asyncio
import aiohttp

'''
解析小说页面
'''

sem = asyncio.Semaphore(10)


class Parser:

    # 解析页码
    def parse_page_list(self):
        print('base parse page list')
        return []

    # 解析页面中的小说数据
    async def async_parse_page(self, url, encoding='utf-8'):
        with await sem:
            async with aiohttp.request('GET', url) as response:
                print(url)
                response = await response.text(encoding=encoding, errors='ignore')
                self.parse_page(response)

    def parse_page(self, response):
        pass

    # 解析小说主页
    async def async_parse_detail(self, url, encoding='utf-8'):
        with await sem:
            with aiohttp.request('GET', url) as response:
                response = await response.text(encoding=encoding, errors='ignore')
                self.parse_detail(response)

    def parse_detail(self, response):
        pass

    def start(self, url, mode, encode):
        print('start')
        loop = asyncio.get_event_loop()
        if mode == 0:
            page_urls = self.parse_page_list()
            total = len(page_urls)
            tasks = []
            for i in range(total):
                page_url = page_urls[i]
                tasks.append(self.async_parse_page(page_url, encode))
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()

        elif mode == 1:
            loop.run_until_complete(self.async_parse_page(url, encode))
            loop.close()

        elif mode == 2:
            loop.run_until_complete(self.async_parse_detail(url, encode))
            loop.close()


