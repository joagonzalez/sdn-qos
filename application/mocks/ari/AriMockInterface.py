from SimpleWebSocketServer import WebSocket

class AriMockApi(WebSocket):
  def handleMessage(self):
      # echo message back to client
      self.sendMessage(self.data)

  def handleConnected(self):
      print(self.address, 'connected')

  def handleClose(self):
      print(self.address, 'closed')
