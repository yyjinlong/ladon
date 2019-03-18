# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from sqlalchemy import text
from oslo_log import log as logging
from osmo.db import get_session, model_query

from stree.db.model import (
    Tpl,
    Node,
    Instance,
    Key,
    Val
)

LOG = logging.getLogger(__name__)


class STreeOperMixin(object):

    def add_node(self, username, data):
        leaf = data.get('leaf')
        pnode = data.get('pnode')
        new_node = data.get('new_node')
        new_node_path = '%s.%s' % (pnode, new_node)
        self._add(username, new_node, new_node_path, leaf, data)

        # NOTE(owt层级, 需自动添加backpool)
        if len(new_node_path.split('.')) == 3 and int(leaf) == 0:
            backpool_path = '%s.backpool' % new_node_path
            print (backpool_path)
            self._add(username, 'backpool', backpool_path, 1, data)

    def _add(self, username, name, new_node_path, leaf, data):
        tpl = data.get('tpl')
        session = get_session()
        with session.begin(subtransactions=True):
            node = session.query(Node)\
                    .filter(Node.name == new_node_path)\
                    .first()
            if not node:
                tpl_obj = session.query(Tpl)\
                        .filter(Tpl.alias == tpl)\
                        .first()
                node = Node()
                node.name = name
                node.tpl_id = tpl_obj.id
                node.leaf = int(leaf)
                node.node = new_node_path
                node.op = data.get('rd')
                node.rd = data.get('op')
                session.add(node)
                LOG.info('** user: %s add new node: %s success.'
                         % (username, new_node_path))

    def del_node(self, username, data):
        node = data.get('node')
        session = get_session()
        with session.begin(subtransactions=True):
            sql = text('select * from tb_node where node <@ :node')
            r = session.execute(sql, {'node': node})
            print (r)
            for row in r:
                print (row)

    def ren_node(self, username, data):
        pass

    def add_instance(self, username, data):
        node = data.get('node')
        ips = data.get('ips')
        ip_list = ips.split('\n')
        session = get_session()
        with session.begin(subtransactions=True):
            instance_list = []
            node_obj = session.query(Node)\
                    .filter(Node.node == node)\
                    .first()
            for ip in ip_list:
                instance = Instance()
                instance.node_id = node_obj.id
                instance.ip = ip
                instance.hostname = 'l-pad.ops.cn9'
                instance_list.append(instance)
            session.add_all(instance_list)


class STreeDataMixin(object):

    def query_tree(self):
        # TODO: 根据用户有权限节点查询
        tree_list = []
        node_list = model_query(Node).all()
        for model in node_list:
            data = {}
            node = model.node
            section_list = node.rsplit('.', 1)
            if len(section_list) == 1:
                root = node
                data['id'] = root
                data['pid'] = root
                data['name'] = root
                data['open'] = True
                data['isParent'] = 0 if model.leaf else 1
                tree_list.append(data)
                continue
            pid = section_list[0]
            name = section_list[1]
            data['id'] = node
            data['pid'] = pid
            data['name'] = name
            data['isParent'] = 0 if model.leaf else 1
            tree_list.append(data)
        expand_node = min(tree_list,
                          key=lambda arg: len(arg.get('id'))).get('id')
        return {
            'tree_list': tree_list,
            'expand_node': expand_node
        }

    def query_tpl(self):
        tpl_list = model_query(Tpl).all()
        return list(map(lambda m: m.alias, tpl_list))

    def query_instance(self, username, data):
        result_list = []
        node = data.get('node')
        offset = data.get('offset')
        session = get_session()
        instances = session.query(Instance).join(Node)\
                .filter(Node.node == node)\
                .order_by(Instance.id)\
                .limit(10)\
                .offset(offset)\
                .all()
        for model in instances:
            hostinfo = {
                'ip': model.ip,
                'hostname': model.hostname,
                'status': model.active,
                'deploy': '',
                'crontab': '',
                'operation': ''
            }
            for item in model.vals:
                if model.id == item.instance_id:
                    hostinfo.update({
                        item.key.key: item.value
                    })
                    break
            result_list.append(hostinfo)
        count = session.query(Instance).join(Node)\
                .filter(Node.node == node)\
                .count()
        return {
            'instances': result_list,
            'total': count
        }

    def query_node_info(self, username, data):
        node = data.get('node')
        session = get_session()
        node_obj = session.query(Node)\
                .filter(Node.node == node)\
                .first()
        return {
            'op': node_obj.op,
            'rd': node_obj.rd,
            'tpl': node_obj.tpl.alias
        }
