from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

# page controller
def index_view(request):
    print(request)
    return '200 OK', [b'Index']


def abc_view(request):
    print(request)
    return '200 OK', [b'ABC']


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 PAGE Not Found']

class Other:

    def __call__(self, request):
        print(request)
        return '200 OK', [b'<h1>other</h1>']

routes = {
    '/': index_view,
    '/abc/': abc_view,
    '/other/': Other()
}

class Application:

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        print('work')
        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view
        request = {}
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes)

with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
