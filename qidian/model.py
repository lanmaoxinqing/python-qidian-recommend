# !/usr/bin/python3
# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase('qidian.db')

class Base(Model):

    class Meta:
        database = db


class Author(Base):
    id = TextField(primary_key=True)
    name = TextField()
    url = TextField(null=True)


class Channel(Base):
    id = TextField(primary_key=True)
    name = TextField()
    url = TextField(null=True)


class Rank(Base):
    type = SmallIntegerField()  # 1 往期强推, 2 往期三江
    fromDate = DateTimeField(null=True)
    toDate = DateTimeField(null=True)


class Book(Base):
    id = TextField(primary_key=True)
    name = TextField()
    url = TextField(null=True)
    channel = ForeignKeyField(Channel, backref="books")
    author = ForeignKeyField(Author, backref="books")


class RankBook(Base):
    rank = ForeignKeyField(Rank)
    book = ForeignKeyField(Book)
    channelName = TextField(null=True)
    bookName = TextField(null=True)
    authorName = TextField(null=True)


class FinishBook(Base):
    book_id = TextField(primary_key=True)
    book_name = TextField()
    book_url = TextField()
    cover_url = TextField(null=True)
    author_id = TextField(null=True)
    author_name = TextField(null=True)
    category = TextField(null=True)
    sub_category = TextField(null=True)
    state = TextField(null=True)
    desc = TextField(null=True)
    state = TextField(null=True)
    word_count = BigIntegerField(default=0)

    def __str__(self):
        print(self.book_name)