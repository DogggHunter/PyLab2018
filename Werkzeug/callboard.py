import os
from urllib.parse import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
import pymongo
from datetime import datetime


class CallBoard(object):
    def __init__(self, conf):
        self.mongo_db = pymongo.MongoClient(conf['host'], conf['port']).ads
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='callboard'),
            Rule('/add', endpoint='add_adt')
        ])

    def on_callboard(self, request):
        ads = self.mongo_db.ads_collection.find()
        return self.render_template('callboard.html', ads=ads)

    def on_add_adt(self, request):
        if request.method == 'POST':
            adt = {
                "title": request.form['title'],
                "description": request.form['description'],
                "date": datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
            }
            self.mongo_db.ads_collection.insert_one(adt)
            return redirect('add')
        return self.render_template('add_adt.html')

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

