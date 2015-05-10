#!/usr/bin/python

import random
import threading
import time
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn


def generate_request_handler(average_latency_seconds, error_ratio):
    def f(self):
        time.sleep(max(0, average_latency_seconds + random.normalvariate(.01, .01)))
        if random.random() < error_ratio:
            self.send_response(500)
        else:
            self.send_response(200)
        self.end_headers()
    return f

def handler_404(self):
  self.send_response(404)

      
ROUTES = {
    ('GET', "/"): lambda self: self.wfile.write("Hello World!"),
    ('GET', "/favicon.ico"): lambda self: self.send_response(404),
    ('GET', "/api/foo"): generate_request_handler(.01, .005),
    ('POST', "/api/foo"): generate_request_handler(.02, .02),
    ('GET', "/api/bar"): generate_request_handler(.015, .00025),
    ('POST', "/api/bar"): generate_request_handler(.05, .01),
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
      ROUTES.get(('GET', self.path), handler_404)(self)

    def do_POST(self):
      ROUTES.get(('POST', self.path), handler_404)(self)
        
class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
      pass

class Server(threading.Thread):
    def run(self):
        httpd = MultiThreadedHTTPServer(('', 8081), Handler)
        httpd.serve_forever()
