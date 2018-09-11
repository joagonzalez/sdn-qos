import sys
import logging
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from AriMockInterface import AriMockApi

class AriMockServer:
    def __init__(self):
        self.port = 8002
        self.host = ''
        try:
            self.server = SimpleWebSocketServer(self.host, self.port, AriMockApi)
            logging.info('Start Ari mock server on port' + repr(self.port))
        except Exception as error:
            logging.error(error)

    def start(self):
        self.server.serveforever()

mock = AriMockServer()
mock.start()
