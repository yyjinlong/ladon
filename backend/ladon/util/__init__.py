# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from datetime import datetime
from enum import Enum, unique

@unique
class Interface(Enum):

    Success = 0
    Failed = 1


@unique
class Operation(Enum):

    ADD_NODE = 0
    DEL_NODE = 1
    REN_NODE = 2
    ADD_HOST = 3
    DEL_HOST = 4
    MOD_PROP = 5


def context(code, msg='', data=[]):
    r = {}
    r['code'] = code
    r['msg'] = msg
    r['data'] = data
    return r


class GlobalSearchBase(object):

    def doc_define(self):
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000+0800')
        doc = {
            '@timestamp': timestamp,
            'node': '',
            'ip': '',
            'hostname': '',
            'deploy': '',
            'crontab': ''
        }
        return doc
