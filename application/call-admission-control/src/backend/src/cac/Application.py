import sys
import logging

from .BaseApplication import BaseApplication

class Application(BaseApplication):
  ''' Start listen in ari and exposes the ws-front-service to webapp '''
  def __init__(self, frontClient):
    BaseApplication.__init__(self, frontClient)

  def getMetrics(self):
    ''' public method that exposes requests to the internal api to the webapp '''
    return self.cacController.doSomething()
  
  def getPorts(self):
    ''' public method that map IP endpoints with physical OpenVSwitch ports
    '''
    return self.cacController.doGetPorts()
    