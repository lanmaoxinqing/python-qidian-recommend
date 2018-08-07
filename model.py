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
