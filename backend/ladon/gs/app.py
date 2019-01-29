# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from osmo.db import get_session
from osmo.base import Application
from oslo_log import log as logging

from ladon.db.model import Node
from ladon.util import GlobalSearchBase
from ladon.util.search import ESHandler

LOG = logging.getLogger(__name__)


class GlobalSearchEngine(Application):
    name = "global search engine"
    version = "v0.1"

    def __init__(self):
        super(GlobalSearchEngine, self).__init__()

    def run(self):
        GlobalSearchUpdater().run()
        LOG.info('....write business data into es success.')


class GlobalSearchUpdater(GlobalSearchBase):

    def __init__(self):
        super(GlobalSearchUpdater, self).__init__()
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
            doc = self.doc_define()
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
                doc = self.doc_define()
                doc.update({'node': node.node})
        self.es_handler.bulk_write(business)
