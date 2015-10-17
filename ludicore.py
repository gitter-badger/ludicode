from player import Player
import uuid

class LudiCore(object):

 
    def __init__(self):
        self.messages={0: "Hello?",
                       1: "Hello!",
                       2: "Games?",
                       3: "Games!",
                       4: "Rules?",
                       5: "Rules",
                       6: "RegisterPlayer?",
                       7: "PlayerRegistered",
                       999: "Error!"}
        
        self.players={}
        
    def sendMessage(self,number, params={}):
        params['message'] = self.messages[number]
        params['uuid']= self.uuid
        return [number,params]

    def createPlayer(self,guid):
        self.players[guid] = Player(guid)
        
    def newUUID(self):
        return uuid.uuid4()

    def isValidFunction(self, number):
        if not (type(number) is int):
            return("Message number is no ordinal number")
        
        if not (number in self.messages):
            return("Message number not found")

        return None

    def error(self, text):
        return self.sendMessage(999, {"description": text})
   
