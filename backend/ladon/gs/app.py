# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

import time
from datetime import datetime

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

LOG = logging.getLogger(__name__)


class GlobalSearchEngine(Application):
    name = "global search engine"
    version = "v0.1"

    def __init__(self):
        super(GlobalSearchEngine, self).__init__()

    def run(self):
        LOG.info('....writing business data into es.')
        data_layer = GloablDataHandler()
        data_layer.make_business_info()
        LOG.info('....write business data into es success.')

    def wait_ctrl_c(self):
        try:
            while True:
                time.sleep(60)
        except:
            pass


class GloablDataHandler(object):

    def __init__(self):
        self.es_handler = ESHandler()

    def make_business_info(self):
        business = []
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000+0800')
        session = get_session()
        nodes = session.query(Node).all()
        for node in nodes:
            for model in node.instances:
                d = {
                    '@timestamp': timestamp,
                    'node': node.node,
                    'ip': model.ip,
                    'hostname': model.hostname,
                    'deploy': '',
                    'crontab': ''
                }
                for item in model.vals:
                    if model.id == item.instance_id:
                        d.update({
                            item.key.key: item.value
                        })
                        break
                business.append(d)
        self.es_handler.bulk_write(business)
