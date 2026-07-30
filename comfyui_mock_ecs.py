#!/usr/bin/env python3
"""ECS本地通路验证Mock服务"""
import json, time
from http.server import HTTPServer, BaseHTTPRequestHandler

class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def _ok(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
         # nginx strips /api/comfy/ prefix, so path could be /status or /api/comfy/status
        if self.path in ('/status', '/api/comfy/status'):
            self._ok({'gpu':'ECS本地通路验证','mode':'local-passthrough','model':'SmolVLA/VLA-T/GR00T(占位)'})
        elif self.path in ('/health', '/api/comfy/health'):
            self._ok({'status':'ok'})
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        cl = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(cl)) if cl > 0 else {}
        if self.path in ('/task', '/api/comfy/task'):
            self._ok({'id':'local-'+str(int(time.time()*1000)),'status':'done','nodes':len(body.get('nodes',[])),'result':'通路验证通过','mode':'local-passthrough'})
        elif self.path in ('/debug', '/api/comfy/debug'):
            self._ok({'step':'本地通路验证','location':'ECS-local','variables':{'nodes':len(body.get('nodes',[]))}})
        else:
            self.send_response(404); self.end_headers()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('MOCK_PORT', 50058))
    print(f'[mock-comfy] port {port}')
    HTTPServer(('127.0.0.1', port), MockHandler).serve_forever()
