"""
This script runs the application using a development server.
"""

import bottle
import os
import sys
import bottle_session
import bottle_redis
import redis
from datetime import datetime
from beaker.middleware import SessionMiddleware

# routes contains the HTTP handlers for our server and must be imported.
import routesDefault

session_opts = {
    'session.type': 'file',
#    'session.type': 'cookie',
    'session.cookie_expires': True,
#    'session.cookie_expires': 300,
    'session.timeout': 3600 * 1,  # 1 hora
    'session.data_dir': './data',
    'session.auto': True
}
app_session = SessionMiddleware(bottle.app(), session_opts)
bottle.default_app = app_session


if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    
    bottle.debug(True)


def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = '10.0.0.103' # remoto
    HOST = 'localhost' # local
    PORT = 8080

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    bottle.run(app=app_session, host=HOST, port=PORT, debug=True)
