# -*- coding: utf-8 -*-
# !/usr/bin/python3

from peewee import *

db = SqliteDatabase('qidian.db')


class Base(Model):

    class Meta:
        database = db


class Author(Base):
    id = TextField(primary_key=True)
    name = TextField()
    url = TextField()


class Channel(Base):
    id = TextField(primary_key=True)
    name = TextField()
    url = TextField()


class Rank(Base):
    type = SmallIntegerField()  # 1 往期强推, 2 往期三江
    fromDate = DateTimeField()
    toDate = DateTimeField()


class Book(Base):
    id = TextField(primary_key=True)
    name = TextField()
    url = TextField()
    channel = ForeignKeyField(Channel, backref="books")
    author = ForeignKeyField(Author, backref="books")


class RankBook(Base):
    rank = ForeignKeyField(Rank)
    book = ForeignKeyField(Book)
    channelName = TextField()
    bookName = TextField()
    authorName = TextField()
