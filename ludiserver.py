#! /usr/bin/python3

import logging
import configparser
import os.path
from flask import Flask, request, Response
from jsonrpcserver import dispatch
from jsonrpcserver.exceptions import InvalidParams
from ludicore import LudiCore
from GameServers import *

class LudiServer(LudiCore):

    ServerVersion='0.0.0'

    GameClasses={}

    def __init__(self):
        
        self.config = configparser.ConfigParser()

        if (os.path.isfile('/home/andy/.ludicode')):
            self.config.read('/home/andy/.ludicode')
        else:
            self.createDefaultConfig('/home/andy/.ludicode')
        self.uuid = self.config['Server']['uuid']
        super(LudiServer,self).__init__()

            
    def createDefaultConfig(self, fname):
        self.config['DEFAULT'] = {'uuid': self.newUUID(),
                             'UserName': 'Frank Nord'}
        self.config['Server'] = {'uuid': self.newUUID(),
                             'ServerName': 'Warpzone MS'}
        # TODO: Schreibfehler abfangen
        with open(fname, 'w') as configfile:
            self.config.write(configfile)

    
    def loadGames(self, vars):

        for cls in vars['Game'].__subclasses__():
            print("Loading GameServer Modules")
            print("Loading: ",cls.__name__,"... ", sep='', end=''),
            self.GameClasses[cls.__name__] = cls
            print("OK")
            print(cls.__doc__, end='\n\n')
            
    def parse(self,function,params):

        error = self.isValidFunction(function)
        print(error)
        if not (error is None):
            return self.error(error)
 
        if (function == 0):
            return self.doHello(params)
        elif (function == 2):
            return self.doGames(params)
        else:
            return self.sendMessage(999,{"description":"Unhandled message"})
            
        
        return self.sendMessage(function, params)

    def doHello(self, params):
        return self.sendMessage(1,{"ServerName": self.config['Server']['servername']})

    def doGames(self, params):
        return self.sendMessage(3,{"GameList": list(self.GameClasses.keys())})
        



    logging.getLogger('jsonrpcserver').setLevel(logging.INFO)
logging.basicConfig()

app = Flask(__name__)

def ludicode(function,params):
    return(srv.parse(function, params))


@app.route('/api', methods=['POST'])
def index():
    print('request')
    r = dispatch([ludicode], request.get_data().decode('utf-8'))
    return Response(r.body, r.http_status, mimetype='application/json')


if __name__ == '__main__':

    print("LudiCode Server v%s" % "0.0.0",end='\n\n')
    srv = LudiServer()
    
    srv.loadGames(vars())

    print()
    print("Waiting for Connections...")
    app.run()

