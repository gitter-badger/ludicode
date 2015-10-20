#! /usr/bin/python3

import configparser
import logging
import os.path
from jsonrpcclient.http_server import HTTPServer
from ludicore import LudiCore

logging.getLogger('jsonrpcclient').setLevel(logging.WARNING)
logging.basicConfig()

class LudiClient(LudiCore):

    
    def __init__(self):
        self.server = HTTPServer('http://127.0.0.1:5000/api')
 

        self.config = configparser.ConfigParser()

        if (os.path.isfile('/home/andy/.ludicode')):
            self.config.read('/home/andy/.ludicode')
        else:
            self.createDefaultConfig('/home/andy/.ludicode')
        self.uuid = self.config[self.game]['uuid']
        super(LudiClient,self).__init__()

            
    def createDefaultConfig(self, fname):
        self.config['DEFAULT'] = {'uuid': self.newUUID(),
                             'UserName': 'Frank Nord'}
        self.config['Server'] = {'uuid': self.newUUID(),
                             'ServerName': 'Warpzone MS'}
        # TODO: Schreibfehler abfangen
        with open(fname, 'w') as configfile:
            self.config.write(configfile)

    def connectToServer(self):
        print("Connecting to Server... " , end = '')
        result = self.server.request('ludicode', self.sendMessage(0))
        if (result[0] == 1):
            print("Ok")
            print("Server: ",result[1]['ServerName'])
            
        print("Requesting available games... ",end='')
        result = self.server.request('ludicode', self.sendMessage(2))
        if (result[0] == 3):
            print("Ok")
            print(', '.join(result[1]['GameList']))
            if (self.game in result[1]['GameList']):
                print(self.game, " is available")
                print("Registering Player (%s)... " % self.config[self.game]['username'],end='')
                result = self.server.request('ludicode', self.sendMessage(6,{"uuid":self.config[self.game]['uuid'],"username":self.config[self.game]['username']}))
                if (result[0] == 7):
                    print("Ok")
                    print("User registered")

                
        # self.sendMessage(0)

class ExampleGame(LudiClient):

    def __init__(self):
        self.game = "TicTacToe"    
        super(ExampleGame,self).__init__()
        
    def play(self):
        self.connectToServer()
                    
if __name__ == '__main__':


    client = ExampleGame()
    client.play()

