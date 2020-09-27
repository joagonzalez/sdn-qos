import sys
import logging

from .ryu.Controller import RyuController
from .ari.CacController import CacController

class BaseApplication:
  ''' Start listen in ari and exposes the ws-front-service to webapp '''
  def __init__(self, frontClient):
    ''' constructor '''
    self.listen = False
    self.frontClient = frontClient
    self.ryuController = RyuController()
    self.cacController = CacController(self.ryuController, self.frontClient)

  def run(self):
    ''' Run Application.
        If Ari connects successfuly, Application state switches to listening Mode On 
    '''
    try:
      self.cacController.run()
      self.listen = True
      logging.info('Start Stasis Application')
    except Exception as error:
      self.listen = False
      logging.error(error)
