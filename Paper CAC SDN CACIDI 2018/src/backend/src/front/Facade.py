from SimpleWebSocketServer import SimpleWebSocketServer
from .WsHandler import WsHandler

class FacadeWsService:
  def __init__(self):
    self.server = None

  def register_command(self, command, name=''):
    WsHandler.register_command(command, name)

  def run(self):
    self.server = SimpleWebSocketServer('', 8000, WsHandler)
    self.server.serveforever()