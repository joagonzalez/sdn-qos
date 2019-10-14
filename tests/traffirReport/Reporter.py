import socket
from logging import info, error
from json import dumps
from threading import Thread

class TrafficReporter:
  # def __init__(self, frontClient):
  def __init__(self):
    # self.frontClient = frontClient
    self.sock = None
    self.buffer_size = 2048
    self.host = 'localhost' # cac-backend IP
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
      print('bind socket to port 9999 success')
      info('Bind socket to port 9999 successfully')
      self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sock.bind( (self.host, self.port) )
      self.listen()
    except socket.error as e:
      error('Error on bind socket')
      error(e)

  # def startListen(self):
  #     nodeHandler = Thread(
  #       target=self.listen
  #     )
  #     nodeHandler.daemon=True
  #     nodeHandler.start()

  def listen(self):
    info('Listen incoming traffic on port 9999')
    self.sock.listen( 1 )
    conn, addr = self.sock.accept() # pylint: disable=W0612
    info('Connection stablished with traffic reporter ' + addr[0] + ':' + str(addr[1]))
    trafficJson = {}
    while True:
      data = str(conn.recv(self.buffer_size)) # pylint: disable=E1101
      lines = data.splitlines()
      for line in lines:
        try:
          print('line' + line)
          if line.count(':') == 2 and ('SIP' in line  or 'RTP' in line):
            (time, protocol) = line.split(' ')
            indexTime = time[0:8]
            print('indexTime: ' + indexTime)
            if trafficJson.get(indexTime) is None:
              trafficJson[indexTime] = { 'sip': 0, 'rtp': 0 }
            if 'SIP' in protocol:
              trafficJson[indexTime]['sip'] += 1
            elif 'RTP' in protocol:
              trafficJson[indexTime]['rtp'] += 1

        except Exception as error:
            print('error in time')
            print(error)
      self.frontClient.broadcast("hostTraffic", {
        "hostTraffic": dumps(data)
      })
      

trafficReporterClient = TrafficReporter()

if __name__ == '__main__':
  trafficReporterClient.listen()