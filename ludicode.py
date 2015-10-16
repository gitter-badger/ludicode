import logging
from flask import Flask, request, Response
from jsonrpcserver import dispatch

logging.getLogger('jsonrpcserver').setLevel(logging.INFO)
logging.basicConfig()

app = Flask(__name__)

def square(x):
    return x * x

def cube(x):
    return x * x * x

@app.route('/api', methods=['POST'])
def index():
    r = dispatch([square, cube], request.get_data().decode('utf-8'))
    return Response(r.body, r.http_status, mimetype='application/json')

if __name__ == '__main__':
    app.port(9277)
    app.run()

# curl -i -X GET -H 'Content-Type: application/json' -d '{"jsonrpc": "2.0", "method": "cube", "params": {"x":3}, "id":5}' http://127.0.0.1:5000/api
