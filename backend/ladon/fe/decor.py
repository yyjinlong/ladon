# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from functools import wraps

from flask import request
from oslo_config import cfg
from osmo.db import get_session

import ladon.util as util
from ladon.util.search import ESHandler
from ladon.db.model import (
    Tpl,
    Node,
    Instance,
    Key,
    Val
)

sync_opts = [
    cfg.ListOpt('hosts', help='kafka host:port pair.'),
    cfg.StrOpt('topic', help='kafka topic for stree sync to es.'),
    cfg.StrOpt('group_id', help='kafka topic for group id to consumer.')
]

CONF = cfg.CONF
CONF.register_opts(sync_opts, 'SYNC')


def sync(param):
    def generator(f):
        @wraps(f)
        def wrap():
            data = request.form
            r = f()
            gss = GloabSearchSync()
            oper_type = param.get('oper_type')
            print ('---------oper type: ', oper_type)
            if oper_type == util.Operation.ADD_NODE:
                gss.sync_node_add(data)
            elif oper_type == util.Operation.DEL_NODE:
                pass
            elif oper_type == util.Operation.REN_NODE:
                pass
            elif oper_type == util.Operation.ADD_HOST:
                gss.sync_host_add(data)
            elif oper_type == util.Operation.DEL_HOST:
                pass
            elif oper_type == util.Operation.MOD_PROP:
                pass
            else:
                pass
            return r
        return wrap
    return generator


class GloabSearchSync(util.GlobalSearchBase):

    def __init__(self):
        super(GloabSearchSync, self).__init__()
        self.es = ESHandler()

    def sync_node_add(self, data):
        pnode = data.get('pnode')
        new_node = data.get('new_node')
        new_node_path = '%s.%s' % (pnode, new_node)
        doc = self.doc_define()
        doc.update({'node': new_node_path})
        self.es.index_write(doc)

    def sync_host_add(self, data):
        packages = []
        node = data.get('node')
        ips = data.get('ips')
        ip_list = ips.split('\n')
        session = get_session()
        instances = session.query(Instance).join(Node)\
                .filter(Node.node == node)\
                .all()
        for model in instances:
            ip = model.ip
            if ip in ip_list:
                doc = self.doc_define()
                doc.update({
                    'node': node,
                    'ip': ip,
                    'hostname': model.hostname
                })
                packages.append(doc)
        self.es.bulk_write(packages)
