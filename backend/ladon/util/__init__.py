# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from enum import Enum, unique


@unique
class Interface(Enum):

    Success = 0
    Failed = 1


def context(code, msg='', data=[]):
    r = {}
    r['code'] = code
    r['msg'] = msg
    r['data'] = data
    return r





