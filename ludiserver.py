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
    print('request')
    r = dispatch([square, cube], request.get_data().decode('utf-8'))
    print(r.body)
    return Response(r.body, r.http_status, mimetype='application/json')

if __name__ == '__main__':
    
    app.run()

