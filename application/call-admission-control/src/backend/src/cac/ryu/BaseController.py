from ..api.service import ApiService
from ...config.settings import config

class BaseController:
  def __init__(self):
    ''' This will make queries to the OF service '''
    self.apiService = ApiService(baseurl=config['ryu']['baseurl'])
