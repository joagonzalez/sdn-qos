import json
from SimpleWebSocketServer import WebSocket

clients = []
commands = {}
class WsHandler(WebSocket):

  @staticmethod
  def register_command(command, name=''):
    commands[name] = command

  def handleMessage(self):
    if self.data in commands.iterkeys():
      commandResponse = commands[self.data]()
      print(commandResponse)
      response = json.dumps(commandResponse)
      self.sendMessage(response)
    
    self.sendMessage(self.data)

  def handleConnected(self):
    clients.append(self)
    print(self.address, 'connected')

  def handleClose(self):
    clients.remove(self)
    print(self.address, 'closed')

