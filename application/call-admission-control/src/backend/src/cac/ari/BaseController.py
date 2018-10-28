import sys
import logging
from threading import Thread

from .Adapter import AriAdapter
from ...config.settings import config

class BaseController:
  def __init__(self, ryuApi, frontClient):
    ''' Stasis Program '''
    self.bridges = []
    self.client = None
    self.ryuApi = ryuApi
    self.frontClient = frontClient

  def subscribe(self, onStartCallback):
    ''' Subscribe Stasis Program and create connection to ari.
        Bind the event listeners for the application '''
    self.connect()
    self.client.on_channel_event('StasisStart', onStartCallback)
    
  def connect(self):
    try:
      self.client = AriAdapter.connect(
        config['ari']['host'],
        config['ari']['username'],
        config['ari']['password']
      )
      logging.info('AriController::Connecting ari service successful')
    except Exception as error:
      logging.error('AriController::Error on connect to ari service::' + repr(error))
      sys.exit()

  def run(self):
    ''' Start listen Stasis App '''
    nodeHandler = Thread(
      target=self.initStasisApplication
    )
    nodeHandler.daemon=True
    nodeHandler.start()

  def initStasisApplication(self):
    ''' Run Cac module in Ari '''
    self.client.run(apps='cac')
