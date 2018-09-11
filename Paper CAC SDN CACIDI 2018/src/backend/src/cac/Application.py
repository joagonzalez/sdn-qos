import sys
import logging

from .ryu.Controller import RyuController
from .ari.Controller import AriController

class Application:
  ''' Start listen in ari and exposes the ws-front-service to webapp '''
  def __init__(self):
    ''' constructor '''
    self.listen = False
    self.args = sys.argv[1:]
    self.ryuController = RyuController()
    self.ariController = AriController(self.ryuController)

  def run(self):
    ''' Run Application.
        If Ari connects successfuly, Application state switches to listening Mode On '''
    try:
      self.ariController.run()
      self.listen = True
      logging.info('Start Stasis Application')
    except Exception as error:
      self.listen = False
      logging.error(error)

  def getMetrics(self):
    ''' public method that exposes requests to the internal api to the webapp '''
    return self.ariController.doSomething()
