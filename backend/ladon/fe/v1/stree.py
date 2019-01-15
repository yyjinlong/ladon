# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from flask import (
    Blueprint,
    session,
    request,
    jsonify
)

import ladon.util as util
from ladon.fe.bll.stree import STreeV1Layer

bp = Blueprint('stree', __name__)


@bp.route('/load/tree', methods=['POST', 'GET'])
def load_tree():
    layer = STreeV1Layer()
    data = layer.display()
    r = util.context(util.Interface.Success.value, data=data)
    return jsonify(r)


@bp.route('/load/tpl', methods=['POST', 'GET'])
def load_tpl():
    layer = STreeV1Layer()
    data = layer.template()
    r = util.context(util.Interface.Success.value, data=data)
    return jsonify(r)


@bp.route('/add/node', methods=['POST', 'GET'])
def add_node():
    username = 'yangjinlong'
    data = request.form
    layer = STreeV1Layer()
    layer.addition(username, data)
    r = util.context(util.Interface.Success.value)
    return jsonify(r)


@bp.route('/del/node', methods=['POST', 'GET'])
def del_node():
    pass


@bp.route('/ren/node', methods=['POST', 'GET'])
def ren_node():
    pass


@bp.route('/load/instance', methods=['POST', 'GET'])
def load_instance():
    username = 'yangjinlong'
    data = request.form
    layer = STreeV1Layer()
    result_info = layer.instance(username, data)
    r = util.context(util.Interface.Success.value, data=result_info)
    return jsonify(r)


@bp.route('/add/instance', methods=['POST', 'GET'])
def add_instance():
    username = 'yangjinlong'
    data = request.form
    layer = STreeV1Layer()
    layer.instance_add(username, data)
    r = util.context(util.Interface.Success.value)
    return jsonify(r)


@bp.route('/load/node/info', methods=['POST', 'GET'])
def load_node_info():
    username = 'yangjinlong'
    data = request.form
    layer = STreeV1Layer()
    result_info = layer.node_info(username, data)
    r = util.context(util.Interface.Success.value, data=result_info)
    return jsonify(r)
