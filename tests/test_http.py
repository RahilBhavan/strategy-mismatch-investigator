import json
import tempfile
import threading
import time
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from app.server import handler
from app.store import Store


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.store=Store(Path(cls.temp.name)/'http.sqlite3')
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),handler(cls.store))
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.temp.cleanup()
    def request(self,path,method='GET',body=None,headers=None):
        data=None if body is None else json.dumps(body).encode()
        request=Request(self.url+path,data=data,method=method,headers=headers or {'Content-Type':'application/json'})
        try:
            with urlopen(request,timeout=10) as response:return response.status,response.read()
        except HTTPError as error:
            code,body=error.code,error.read();error.close();return code,body
    def test_end_to_end_public_api(self):
        _,body=self.request('/api/cases/status');source=json.loads(body)
        status,body=self.request('/api/jobs','POST',dict(case_id='status',fingerprint=source['fingerprint'],phase='diagnose',mode='normal'))
        self.assertEqual(status,202);job=json.loads(body)
        for _ in range(100):
            _,body=self.request('/api/jobs/'+job['id']);job=json.loads(body)
            if job['state']=='complete':break
            time.sleep(.02)
        self.assertEqual(job['result']['status'],'demonstrated')
        status,body=self.request('/api/jobs/'+job['id']+'/export');self.assertEqual(status,200)
        status,reopened=self.request('/api/restore','POST',json.loads(body));self.assertEqual(status,201)
        self.assertEqual(json.loads(reopened)['result']['residual'],'0.00')
    def test_intake_and_origin(self):
        status,body=self.request('/api/jobs','POST',{})
        self.assertEqual(status,400)
        status,_=self.request('/api/cases','POST',{},dict(Origin='https://unrelated.invalid',**{'Content-Type':'application/json'}))
        self.assertEqual(status,403)
        status,_=self.request('/api/jobs/nope');self.assertEqual(status,404)
        status,_=self.request('/../../.local/poc.sqlite3');self.assertEqual(status,404)
    def test_static_app(self):
        status,body=self.request('/')
        self.assertEqual(status,200)
        self.assertIn(b'Proof of concept',body)
        status,body=self.request('/contract.html');self.assertEqual(status,200)
        self.assertIn(b'locally designed',body)
