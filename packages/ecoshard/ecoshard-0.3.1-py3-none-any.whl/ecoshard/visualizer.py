"""Entry point for ecoshard."""
import os
import sys
import logging

import taskgraph
from flask import Flask
import flask

APP = Flask(__name__)
APP.config['SECRET_KEY'] = b'\xe2\xa9\xd2\x82\xd5r\xef\xdb\xffK\x97\xcfM\xa2WH'
VISITED_POINT_ID_TIMESTAMP_MAP = {}
ACTIVE_USERS_MAP = {}
WORKSPACE_DIR = 'workspace_ecoshard_visualizer'
DATA_STORE_DIR = 'datastore'
VALIDATION_DATABASE_PATH = os.path.join(WORKSPACE_DIR)
DATABASE_PATH = os.path.join(WORKSPACE_DIR, 'dam_bounding_box_db.db')
N_WORKERS = -1
REPORTING_INTERVAL = 5.0

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format=('%(message)s'),
    stream=sys.stdout)
logging.getLogger('ecoshard').setLevel(logging.WARN)
LOGGER = logging.getLogger(__name__)

@APP.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(
        os.path.join(APP.root_path, 'images'), 'favicon.ico',
        mimetype='image/vnd.microsoft.icon')

@APP.route('/<string:ecoshard_id>/<string:style_id>')
def ecoshard_with_style(ecoshard_id, style_id):
    """Entry point."""
    LOGGER.info('ecoshard with style: %s %s', ecoshard_id, style_id)
    datastore_id = ecoshard_id.split(':')[0]
    layer_id = ecoshard_id
    return flask.render_template(
        'ecoshard.html', **{
            'datastore_id': datastore_id,
            'layer_id': layer_id,
            'style_id': style_id,
        })

@APP.route('/<string:ecoshard_id>')
def ecoshard(ecoshard_id):
    """Entry point."""
    LOGGER.info('ecoshard as: %s', ecoshard_id)
    datastore_id = ecoshard_id.split(':')[0]
    layer_id = ecoshard_id
    return flask.render_template(
        'ecoshard.html', **{
            'datastore_id': datastore_id,
            'layer_id': layer_id,
            'style_id': '',
        })


if __name__ == '__main__':
    DB_CONN_THREAD_MAP = {}
    TASK_GRAPH = taskgraph.TaskGraph(
        WORKSPACE_DIR, N_WORKERS, reporting_interval=REPORTING_INTERVAL)
    APP.run(host='0.0.0.0', port=8888)
    # this makes a connection per thread
