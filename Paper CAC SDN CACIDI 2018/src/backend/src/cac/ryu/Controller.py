from ..api.service import ApiService

class RyuController:
  def __init__(self):
    ''' This will make queries to the OF service '''
    self.apiService = ApiService(baseurl='http://192.168.0.187:8080')

  def queryForGetNodes(self):
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
