"""Bounded, loopback HTTP service for the standalone seismic workspace."""
import json
import mimetypes
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket
import threading
from urllib.parse import urlparse
import numpy as np
from .model import compare
from .benchmark import REPORT_DIR, saved_report

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
MAX_BODY_BYTES = 2_000_000


class LocalServer(ThreadingHTTPServer):
    daemon_threads = True

    def server_bind(self):
        if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            self.allow_reuse_address = False
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


def create_server(host='127.0.0.1', port=8767):
    gate = threading.Lock()
    files = {path: WEB / path.lstrip('/') for path in (
        '/index.html', '/seismic.css', '/seismic.js', '/theme.css',
        '/records/el-centro-1940.at2', '/records/README.md')}
    files['/'] = WEB / 'index.html'
    files.update({f'/api/seismic-validation/{url}': REPORT_DIR / name for url, name in (
        ('report.md', 'report.md'), ('comparison.png', 'opensees-comparison.png'),
        ('convergence.png', 'time-step-convergence.png'))})

    class Handler(BaseHTTPRequestHandler):
        def respond(self, body, code=200, media='application/json', headers=None):
            self.send_response(code)
            self.send_header('Content-Type', media)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, value, code=200, headers=None):
            self.respond(json.dumps(value, allow_nan=False).encode(), code, headers=headers)

        def do_GET(self):
            path = urlparse(self.path).path
            if path == '/api/health':
                return self.send_json({'ok': True, 'application': 'stratum-seismic', 'mode': 'local'})
            if path == '/api/seismic-validation':
                return self.send_json(saved_report())
            file = files.get(path)
            if file is None or not file.is_file():
                return self.send_json({'error': 'Not found'}, 404)
            media = mimetypes.guess_type(file.name)[0] or 'text/plain; charset=utf-8'
            self.respond(file.read_bytes(), media=media)

        def do_POST(self):
            if urlparse(self.path).path != '/api/seismic':
                return self.send_json({'error': 'Not found'}, 404)
            try:
                size = int(self.headers.get('Content-Length', 0))
                if size > MAX_BODY_BYTES:
                    return self.send_json({'error': 'Request exceeds 2 MB limit'}, 413)
                if size < 1:
                    raise ValueError('A JSON request body is required')
                def reject_nonfinite(value):
                    raise ValueError('JSON numbers must be finite')
                request = json.loads(self.rfile.read(size), parse_constant=reject_nonfinite)
                if not isinstance(request, dict):
                    raise ValueError('JSON request must be an object')
                if not gate.acquire(blocking=False):
                    return self.send_json({'error': 'Analysis is busy; retry shortly'}, 429,
                                          headers={'Retry-After': '2'})
                try:
                    result = compare(request)
                finally:
                    gate.release()
                return self.send_json(result)
            except (ValueError, TypeError, KeyError, IndexError, OverflowError,
                    UnicodeDecodeError, np.linalg.LinAlgError) as error:
                return self.send_json({'error': str(error)}, 400)

    return LocalServer((host, port), Handler)


def serve(host='127.0.0.1', port=8767):
    server = create_server(host, port)
    print(f'STRATUM Seismic running at http://{host}:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
