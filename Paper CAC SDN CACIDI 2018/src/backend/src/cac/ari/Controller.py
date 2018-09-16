import sys
import logging
import ari
from threading import Thread

connectedChannels = {}
totalChannels = 0

class AriController:
  def __init__(self, ryuApi, frontClient):
    ''' Stasis Program '''
    self.base_url = 'http://192.168.0.163:8088/'
    self.username = 'asterisk'
    self.password = 'asterisk'
    self.bridges = []
    self.client = None
    self.ryuApi = ryuApi
    self.frontClient = frontClient
    self.setup()

  def connect(self):
    print('iniciando conexion')
    try:
      logging.info('Connecting ari service successful')
      return ari.connect(self.base_url, self.username, self.password)
    except Exception as error:
      print(error)
      logging.error('Error on connect ari service::' + repr(error))
      sys.exit()
  
  def doSomething(self):
    response = self.ryuApi.queryForGetNodes()
    return response

  def doGetPorts(self):
    response = self.ryuApi.queryForGetPorts()
    return response

  def onStartCallback(self, channel_obj, event):
    ''' initialize channels and events. Aca va la logica de los scripts que viste en los exapmles '''
    print('onStartCallback')
    channel = channel_obj.get('channel')
    connectedChannels[ channel.json.get('name') ] = True
    print "Channel %s has entered the application" % channel.json.get('name')
    
    self.frontClient.broadcast("newChannel", {
      "currentNewChannel": channel.json.items(),
      "totalChannels": self.getTotalChannels()
    })

  def onEndCallback(self, channel, event):
    ''' Hangout bridges, channels and stop listening. Clean stuff '''
    connectedChannels[ channel.json.get('name') ] = False
    self.frontClient.broadcast("closeChannel", {
      "totalChannels": self.getTotalChannels()
    })

  def getTotalChannels(self):
    localChannels = 0
    for connectedChannel in connectedChannels:
      print("connectedCHannel?", connectedChannels[connectedChannel])
      if connectedChannels[connectedChannel]:
        localChannels = localChannels + 1
    
    totalChannels = localChannels
    return totalChannels

  def setup(self):
    ''' Setup Stasis Program. Create connection to ari and bind the listen events for the application '''
    self.client = self.connect()
    self.client.on_channel_event('StasisStart', self.onStartCallback)
    self.client.on_channel_event('StasisEnd', self.onEndCallback)
    
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
