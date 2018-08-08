# !/usr/bin/python3
# -*- coding: utf-8 -*-

from peewee import *
import asyncio

db = SqliteDatabase('jinjiang.db')
host = 'http://www.jjwxc.net'
sem = asyncio.Semaphore(5)


class Base(Model):

    class Meta:
        database = db


class FreeRank(Base):
    id = TextField(primary_key=True)
    book_name = TextField()
    book_url = TextField()
    author_name = TextField(null=True)
    author_url = TextField(null=True)
    category = TextField(null=True)
    tag = TextField(null=True)
    state = TextField(null=True)
    recommend_reason = TextField(null=True)
    word_count = BigIntegerField(null=True)
    collect_count = BigIntegerField(null=True)


class VipRank(Base):
    id = TextField(primary_key=True)
    book_name = TextField()
    book_url = TextField()
    author_name = TextField(null=True)
    author_url = TextField(null=True)
    category = TextField(null=True)
    tag = TextField(null=True)
    state = TextField(null=True)
    recommend_reason = TextField(null=True)
    word_count = BigIntegerField(null=True)
    collect_count = BigIntegerField(null=True)


