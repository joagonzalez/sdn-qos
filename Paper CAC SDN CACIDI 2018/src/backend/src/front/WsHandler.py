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
      response = json.dumps(commandResponse)
    else:
      response = json.dumps(self.data)
    
    for client in self.server.connections.itervalues():
      try:
        client.sendMessage(response)
      except Exception as n:
        print n

  def handleConnected(self):
    clients.append(self)
    print(self.address, 'connected')

  def handleClose(self):
    clients.remove(self)
    print(self.address, 'closed')

