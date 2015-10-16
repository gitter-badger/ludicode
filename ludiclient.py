import logging
from jsonrpcclient.http_server import HTTPServer

logging.getLogger('jsonrpcclient').setLevel(logging.INFO)
logging.basicConfig()

server = HTTPServer('http://127.0.0.1:5000/api')
result = server.request('cube', x=3)

print(result)
