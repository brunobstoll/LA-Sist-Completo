
import bottle
import os
import sys
from bottle import default_app
import bottle_session
#import bottle_redis
#import redis
from datetime import datetime
from beaker.middleware import SessionMiddleware

# routes contains the HTTP handlers for our server and must be imported.
import routesDefault

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.timeout': 3600 * 1,  # 1 hora
    'session.data_dir': './data',
    'session.auto': True
}
app_session = SessionMiddleware(bottle.app(), session_opts)
#bottle.default_app = app_session

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')

    return bottle.static_file(filepath, root=STATIC_ROOT)


# A very simple Bottle Hello World app for you to get started with...
#from bottle import default_app, route

#@route('/')
#def hello_world():
#    return 'Hello from Bottle! <br>Atenção'

#application = default_app()
application = app_session

