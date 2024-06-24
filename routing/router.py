"""
httpリクエストを受け取る処理。このモジュールを読み込み、
@router.route()デコレータを使ってルーティングを設定することで、
httpリクエストを受け取ることができる。
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.parse import urlparse, parse_qs

class Router:
    def __init__(self):
        self._routes = {}

    def route(self, path, method='GET'):
        def wrapper(handler):
            self._routes[path] = {
                'handler': handler,
                'method': method
            }
            return handler
        return wrapper

    def run(self, host='0.0.0.0', port='8080'):
        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.handle_request('GET')

            def do_POST(self):
                self.handle_request('POST')

            def do_PUT(self):
                self.handle_request('PUT')

            def do_DELETE(self):
                self.handle_request('DELETE')

            def handle_request(self, method):
                path = urlparse(self.path).path
                # 登録されているルーティングの中から、リクエストされたパスから始まり、メソッドに一致するものを探す
                if path in self.server._routes and self.server._routes[path]['method'] == method:
                    self.server._routes[path]['handler'](self)
                self.send_response(404)
                self.end_headers()

        self.server = HTTPServer((host, port), RequestHandler)
        self.server._routes = self._routes
        self.server.serve_forever()

def get_router():
    """Routerクラスをシングルトンで返す"""
    if not hasattr(get_router, 'router'):
        get_router.router = Router()
    return get_router.router