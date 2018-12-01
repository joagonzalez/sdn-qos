import sys
import socket
import logging
import json
from threading import Thread

class NetworkTrafficRender:
  def __init__(self, frontClient):
    self.frontClient = frontClient
    self.sock = None
    self.host = '172.18.0.13' # cac-backend IP
    self.port = 9999
    self.openSocket()

  def openSocket(self):
    ''' Create ipV4 socket that handle STREAM '''
    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.bind()
      logging.info('Socket created successful')
    except socket.error as e:
      logging.error('Error on create socket')
      logging.error(e)
      sys.exit()
  
  def bind(self):
    ''' Bind socket '''
    try:
      print('Starting server...')
      logging.info('starting server...')
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind( (self.host, self.port) )
      nodeHandler = Thread(
        target=self.read
      )
      nodeHandler.daemon=True
      nodeHandler.start()
    except socket.error as e:
      logging.error('Error on connect to socket...')
      logging.error(e)
      sys.exit()
  
  def read(self):
    ''' Start read buffer '''
    print('read tcpdump buffer')
    logging.info('read tcpdump buffer')
    self.sock.listen( 1 )
    while True:
      conn, addr = self.sock.accept()
      data = conn.recv(2048).decode()
      if data is not None:
        print('data!!!:::::::')
        print(data)
        self.frontClient.broadcast("hostTraffic", {
          "hostTraffic": json.dumps(data)
        })