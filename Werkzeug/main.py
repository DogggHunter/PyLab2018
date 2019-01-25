import os
from callboard import CallBoard
from werkzeug.wsgi import SharedDataMiddleware


def create_app(host='localhost', port=27017, with_static=True):
    app = CallBoard({
        'host':       host,
        'port':       port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
