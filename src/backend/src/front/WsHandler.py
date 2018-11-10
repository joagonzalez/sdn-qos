import json
from SimpleWebSocketServer import WebSocket

commands = {}
class WsHandler(WebSocket):

  @staticmethod
  def register_command(command, name=''):
    commands[name] = command

  def handleMessage(self):
    if self.data in commands.iterkeys():
      commandResponse = commands[self.data]()
      response = commandResponse
    else:
      response = self.data
    
    for client in self.server.connections.itervalues():
      try:
        client.sendMessage(response)
      except Exception as n:
        print n

  def handleConnected(self):
    print(self.address, 'connected')

  def handleClose(self):
    print(self.address, 'closed')

