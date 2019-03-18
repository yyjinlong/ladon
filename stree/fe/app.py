# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

import os
from datetime import timedelta

from flask_cors import CORS
from oslo_log import log as logging
from osmo.wsgi import WSGIApplication

LOG = logging.getLogger(__name__)


class STreeWebApplication(WSGIApplication):
    name = 'stree wsgi'
    version = 'v0.1'

    def init_flask(self):
        super(STreeWebApplication, self).init_flask()

        app = self.flask_app
        CORS(app, resources=r'/*')
        app.static_url_path = '/static'
        app.secret_key = 'stree wsgi application'
        app.permanent_session_lifetime = timedelta(hours=2)

        LOG.info('** Fe web flask app root path: %s' % app.root_path)
        ui_path = os.path.join(app.root_path, 'stree-ui')
        st_path = os.path.join(ui_path, 'static')
        LOG.info('** Fe web flask template path: %s' % ui_path)
        LOG.info('** Fe web flask static path: %s' % st_path)
        app.template_folder = ui_path
        app.static_folder = st_path

        import stree.fe.v1.index as index
        app.register_blueprint(index.bp, url_prefix='')

        import stree.fe.v1.stree as stree
        app.register_blueprint(stree.bp, url_prefix='/stree/api/v1')
