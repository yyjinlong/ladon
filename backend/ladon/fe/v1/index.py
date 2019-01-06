# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

from flask import (
    request,
    Blueprint,
    render_template
)

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
