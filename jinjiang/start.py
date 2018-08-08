# -*- coding: utf-8 -*-
# !/usr/bin/python3


try:
    import jinjiang.free_rank_parser as free_rank_parser
    import jinjiang.vip_rank_parser as vip_rank_parser
    from .model import *
except:
    import free_rank_parser
    import vip_rank_parser
    from model import *


db.connect()
vip_rank_parser.update()
db.close()


