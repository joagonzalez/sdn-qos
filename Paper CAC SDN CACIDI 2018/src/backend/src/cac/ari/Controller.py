import sys
import logging
import ari
from threading import Thread

class AriController:
  def __init__(self, ryuApi):
    ''' Stasis Program '''
    self.base_url = 'http://192.168.163:8088/'
    self.username = 'asterisk'
    self.password = 'asterisk'
    self.bridges = []
    self.client = None
    self.ryuApi = ryuApi
    self.setup()

  def connect(self):
    print('iniciando conexion')
    try:
      return ari.connect(self.base_url, self.username, self.password)
      print('conectando')
      logging.info('Connecting ari service successful')
    except Exception as error:
      print('error')
      print(error)
      logging.error('Error on connect ari service::' + repr(error))
      sys.exit()
  
  def doSomething(self):
    response = self.ryuApi.queryForGetNodes()
    print('respuesta del Ryu::queryForGetNodes')
    print(response)
    return response

  def onStartCallback(self, channel, event):
    ''' initialize channels and events. Aca va la logica de los scripts que viste en los exapmles '''
    print('onStartCallback')
    print(channel)
    print(event)
    currentChannel = channel.get('channel')
    print "Channel %s has entered the application" % currentChannel.json.get('name')
 
    for key, value in channel.json.items():
        print "%s: %s" % (key, value)

  def onEndCallback(self, channel, event):
    ''' Hangout bridges, channels and stop listening. Clean stuff '''

  def setup(self):
    ''' Setup Stasis Program. Create connection to ari and bind the listen events for the application '''
    self.client = self.connect()
    self.client.on_channel_event('StasisStart', self.onStartCallback)
    
  def init(self):
    self.client.run(apps='cac')

  def run(self):
    ''' Connect to Ari Websocket and registers as "cac" Module
        in order to be able to be used in extensions.conf '''
    nodeHandler = Thread(
      target=self.init
    )
    nodeHandler.daemon=True
    nodeHandler.start()
