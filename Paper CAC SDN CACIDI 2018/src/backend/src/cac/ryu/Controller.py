from ..api.service import ApiService

class RyuController:
  def __init__(self):
    ''' This will make queries to the OF service '''
    self.apiService = ApiService(baseurl='http://localhost:8080')

  def queryForGetNodes(self):
    ''' this do queries '''
    return self.apiService.get(
      endpoint='/stats/desc/1'
    )
