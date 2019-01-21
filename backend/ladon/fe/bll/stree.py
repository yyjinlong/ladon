# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#


from osmo.db import get_session

from ladon.db.model import (
    Tpl,
    Node,
    Instance,
    Key,
    Val
)
from ladon.util.search import ESHandler
from ladon.fe.bll.base import STreeOperMixin, STreeDataMixin


class STreeV1Layer(STreeOperMixin, STreeDataMixin):

    def display(self):
        result_info = self.query_tree()
        return result_info

    def template(self):
        result_info = self.query_tpl()
        return result_info

    def addition(self, username, data):
        self.add_node(username, data)

    def instance(self, username, data):
        result_info = self.query_instance(username, data)
        return result_info

    def instance_add(self, username, data):
        self.add_instance(username, data)

    def node_info(self, username, data):
        result_info = self.query_node_info(username, data)
        return result_info

    def query(self, username, data):
        lucene = data.get('lucene')
        es_handler = ESHandler()
        result_info = es_handler.query(lucene)
        return result_info
