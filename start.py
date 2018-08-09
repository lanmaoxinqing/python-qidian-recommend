# -*- coding: utf-8 -*-
# !/usr/bin/python3

import argparse
import qidian.finish_parser as fp
import html

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('url', default=' ')
arg_parse.add_argument('-m', dest='mode', default=0)
arg_parse.add_argument('-e', dest='encode', default='utf-8')

args = arg_parse.parse_args()

parser = fp.FinishParser()
parser.start(args.url, args.mode, args.encode)

