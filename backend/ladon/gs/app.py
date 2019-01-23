# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

import time
from datetime import datetime

from oslo_config import cfg
from osmo.db import get_session
from osmo.base import Application
from oslo_log import log as logging

from ladon.db.model import (
    Tpl,
    Node,
    Instance,
    Key,
    Val
)
from ladon.util.search import ESHandler

sync_opts = [
    cfg.StrOpt('sync_mode',
               default='full',
               choices=('full', 'update'),
               help='STree business data sync to elasticsearch mode. '
                    'default `full`, choices=(`full`, `update`).')
]

CONF = cfg.CONF
CONF.register_cli_opts(sync_opts)

LOG = logging.getLogger(__name__)


class GlobalSearchEngine(Application):
    name = "global search engine"
    version = "v0.1"

    def __init__(self):
        super(GlobalSearchEngine, self).__init__()

    def run(self):
        if CONF.sync_mode == 'full':
            GloablFullDataHandler().run()
        elif CONF.sync_mode == 'update':
            GloablUpdateDataHandler().run()
        LOG.info('....write business data into es success.')

    def wait_ctrl_c(self):
        try:
            while True:
                time.sleep(60)
        except:
            pass


class GlobalDataBase(object):

    def _doc_define(self):
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


class GloablFullDataHandler(GlobalDataBase):

    def __init__(self):
        super(GloablFullDataHandler, self).__init__()
        self.es_handler = ESHandler()

    def run(self):
        self.es_handler.delete_index()
        self.es_handler.create_index()
        self.write_business_info()

    def write_business_info(self):
        business = []
        session = get_session()
        nodes = session.query(Node).all()
        for node in nodes:
            doc = self._doc_define()
            doc.update({'node': node.node})
            if not node.instances:
                business.append(doc)
                continue
            for model in node.instances:
                doc.update({
                    'ip': model.ip,
                    'hostname': model.hostname
                })
                for item in model.vals:
                    if model.id == item.instance_id:
                        doc.update({
                            item.key.key: item.value
                        })
                        break
                business.append(doc)
                doc = self._doc_define()
                doc.update({'node': node.node})
        self.es_handler.bulk_write(business)


class GloablUpdateDataHandler(GlobalDataBase):

    def __init__(self):
        super(GloablUpdateDataHandler, self).__init__()
        self.es_handler = ESHandler()

    def run(self):
        # TODO: 从kafka读取消息
        print ('........update data')

    def write_business_info(self, data):
        # TODO: 基于doc_define更新数据
        doc = self._doc_define()
        package = {}
        self.es_handler.index_write(package)
