# -*- coding: utf-8 -*-
# !/usr/bin/python3

from qidian_model import *
from wordcloud import WordCloud
import jieba

db.connect()
rankbooks = RankBook.select(RankBook.bookName)
db.close()
names = []
for name in rankbooks.tuples():
    names.append(name[0])

seg_list = jieba.cut("".join(names))
words = " ".join(seg_list)

result = WordCloud(font_path="/System/Library/Fonts/PingFang.ttc",
                   width=600,
                   height=300,
                   margin=10,
                   background_color="white",
                   random_state=10
                   ).generate(words)
result.to_file('1.png')
