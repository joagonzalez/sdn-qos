import socket
from logging import info, error
from json import dumps
from threading import Thread

class TrafficReporter:
  def __init__(self, frontClient):
    self.frontClient = frontClient
    self.sock = None
    self.buffer_size = 2048 # tambien puede ser 4096
    self.host = '172.18.0.13' # cac-backend IP
    self.port = 9999
    self.init()

  def init(self):
    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.bind()
      info('Socket created successfully')
    except socket.error as e:
      error('Error on create socket')
      error(e)
  
  def bind(self):
    try:
      info('Bind socket to port 9999 successfully')
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind( (self.host, self.port) )
      nodeHandler = Thread(
        target=self.listen
      )
      nodeHandler.daemon=True
      nodeHandler.start()
    except socket.error as e:
      error('Error on bind socket')
      error(e)

  def listen(self):
    info('Listen incoming traffic on port 9999')
    self.sock.listen( 1 )
    conn, addr = self.sock.accept() # pylint: disable=W0612
    info('Connection stablished with ' + addr[0] + ':' + str(addr[1])
    while True:
      data = conn.recv(self.buffer_size).decode() # pylint: disable=E1101
      if data is not None:
        self.frontClient.broadcast("hostTraffic", {
          "hostTraffic": dumps(data)
        })
