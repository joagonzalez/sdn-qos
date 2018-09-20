import sys
import logging
import ari
from threading import Thread
from ...config.settings import config
from .StasisApp import stasis_start_cb

class AriController:
  ''' Esta clase crea la conexion con el Ari y setea la logica del programa Stasis '''
  ''' El stasis se podria poner en Otra clase y la API en un Facade que extienda de Ari
      @TODO: tiene que haber un AriControllerBase que sea este mismo pero sin la api publica '''
  def __init__(self, ryuApi, frontClient):
    ''' Stasis Program '''
    self.bridges = []
    self.client = None
    self.ryuApi = ryuApi
    self.frontClient = frontClient
    self.setup()

  def setup(self):
    ''' Setup Stasis Program. Create connection to ari and bind the listen events for the application '''
    self.connect()
    self.client.on_channel_event('StasisStart', self.onStartCallback)
    
  def connect(self):
    try:
      self.client = ari.connect(
        config['ari']['host'],
        config['ari']['username'],
        config['ari']['password']
      )
      logging.info('AriController::Connecting ari service successful')
    except Exception as error:
      logging.error('AriController::Error on connect to ari service::' + repr(error))
      sys.exit()

  def onStartCallback(self, channel_obj, event):
    ''' initialize channels and events. Aca va la logica de los scripts que viste en los exapmles '''
    print('onStartCallback')
    stasis_start_cb(channel_obj, event, self.client, self.frontClient, self.ryuApi)

  def run(self):
    ''' Start listen Stasis App '''
    nodeHandler = Thread(
      target=self.initStasisApplication
    )
    nodeHandler.daemon=True
    nodeHandler.start()

  def initStasisApplication(self):
    ''' Connect to Ari Websocket and registers as "cac" Module
        in order to be able to be used in extensions.conf '''
    ''' Runs the stasis application in the Ari '''
    self.client.run(apps='cac')
  
  def doSomething(self):
    ''' esto deberia moverse al Facade que expone el metodo '''
    response = self.ryuApi.queryForGetNodes()
    return response

  def doGetPorts(self):
    ''' esto deberia moverse al Facade que expone el metodo '''
    return self.ryuApi.queryForGetPorts()
