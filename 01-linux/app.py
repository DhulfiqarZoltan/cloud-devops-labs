# Author: Dr. Alwahab Dhulfiqar Zoltan
"""Cloud Lab: a deliberately small, local teaching application."""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/health'):
            self.send_error(404)
            return
        body = b'OK\n' if self.path == '/health' else b'Hello, cloud students!\n'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    HTTPServer((os.getenv('BIND', '127.0.0.1'), int(os.getenv('PORT', '8000'))), Handler).serve_forever()
