import sys
import logging

from .BaseApplication import BaseApplication

class Application(BaseApplication):
  ''' 
  Start listen in ari and exposes the ws-front-service to webapp 
  '''

  def __init__(self, frontClient):
    BaseApplication.__init__(self, frontClient)

  def getTopologyLinks(self):
    ''' 
    Get topology links 
    '''
    return self.cacController.getTopologyLinks()
  
  def getTopologySwitches(self):
    ''' 
    Get topology open flow switches
    '''
    return self.cacController.getTopologySwitches()

  def toggleCac(self):
    '''
    Feature flag for call admission control
    '''
    self.cacController.cacEnable = not self.cacController.cacEnable

  def toggleQos(self):
    '''
    Feature flag for quality of service
    '''
    self.cacController.qosEnable = not self.cacController.qosEnable

    