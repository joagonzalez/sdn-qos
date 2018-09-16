from threading import Thread
import time

from SimpleWebSocketServer import SimpleWebSocketServer
from .WsHandler import WsHandler
from ..config.settings import config

class FacadeWsService:
  def __init__(self):
    self.server = None

  def register_command(self, command, name=''):
    WsHandler.register_command(command, name)

  def run(self, Client):
    nodeHandler = Thread(
      target=self.startServer
    )
    nodeHandler.daemon=True
    nodeHandler.start()
    time.sleep(1)
    Client.connect()

  def startServer(self):
    self.server = SimpleWebSocketServer(
      config['frontService']['host'],
      config['frontService']['listen'],
      WsHandler
    )
    self.server.serveforever()