# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

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
