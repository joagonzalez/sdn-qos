from ..api.service import ApiService
from ...config.settings import config
from .BaseController import BaseController

class RyuController(BaseController):
  def queryForGetNodes(self):
    ''' los endpoints podrian estar registrados en un archivo Routes.. dentro de la carpeta Ryu? '''
    ''' this do queries '''
    return self.apiService.post(
      endpoint='/stats/flow/1',
      data={
        "match": {
          "in_port": 1
        }
      }
    )
  
  def queryForGetPorts(self):
    ''' query that maps IP from asterisk endpoints
        with phyisical ports and MAC of OpenVSwitches
    '''
    return self.apiService.get(
      endpoint = '/simpleswitch/iptoporttable/0000000000000001'
    )
