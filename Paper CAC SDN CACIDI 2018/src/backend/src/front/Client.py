from json import dumps
import websocket
from ...config.settings import config

try:
    import thread
except ImportError:
    import _thread as thread
import time

class Client:
  def __init__(self):
    self.connection = None
    self.connected = False

  def connect(self):
    # websocket.enableTrace(True)
    self.connection = websocket.WebSocketApp(config['client']['baseurl'],
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
    self.connection.on_open = self.on_open
    self.connection.run_forever()

  def on_message(self, message):
    print('Client::onmessage')
    print(message)

  def on_error(self, error):
    print(error)

  def on_close(self):
    print("### closed ###")

  def on_open(self):
    self.connection.send("Hello")

  def broadcast(self, notificationType, data):
    message = {
      "notificationType": notificationType,
      "data": data
    }
    self.connection.send(dumps(message))

  def disconnect(self):
    self.connection.close()
