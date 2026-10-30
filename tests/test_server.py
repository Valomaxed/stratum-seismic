"""Standalone service integration checks; no truss or ML artifacts required."""
import json
import http.client
import threading
import unittest
import urllib.request
import urllib.error
from seismic_frame.server import create_server


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, path, body=None):
        data = None if body is None else body.encode()
        req = urllib.request.Request(self.base+path, data=data,
                                     headers={'Content-Type': 'application/json'})
        try:
            response = urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, response.headers, response.read()

    def test_workspace_health_and_static_boundary(self):
        status, headers, page = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn(b'STRATUM Seismic', page)
        self.assertEqual(headers['Cache-Control'], 'no-store')
        health = self.request('/api/health')
        self.assertEqual(json.loads(health[2])['application'], 'stratum-seismic')
        for path in ('/seismic_frame/model.py', '/../README.md', '/.env',
                     '/api/seismic-validation/histories.npz', '/api/models'):
            self.assertEqual(self.request(path)[0], 404)

    def test_analysis_and_invalid_requests(self):
        record = {'text': 'ACCELERATION IN UNITS OF G\nNPTS= 3, DT= .02 SEC\n0 .1 0', 'unit': 'g'}
        status, _, body = self.request('/api/seismic', json.dumps({'record': record}))
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)['systems']), 3)
        for body in ('[]', '{invalid', '{"scale_factor": NaN}', '{}'):
            self.assertEqual(self.request('/api/seismic', body)[0], 400)
        self.assertEqual(self.request('/api/analyze', '{}')[0], 404)
        # The service rejects an oversized Content-Length before reading a body.
        # Send headers only: writing a 2 MB body after an early 413 can race the
        # closed HTTP/1.0 socket and raise BrokenPipeError on some platforms.
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=10)
        try:
            connection.request('POST', '/api/seismic', headers={'Content-Length': '2000001'})
            response = connection.getresponse()
            self.assertEqual(response.status, 413)
            response.read()
        finally:
            connection.close()


if __name__ == '__main__':
    unittest.main()
