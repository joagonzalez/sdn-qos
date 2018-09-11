import pycurl
from StringIO import StringIO
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

class ApiService:
  def __init__(self, baseurl):
    ''' THis is an abstraction that wrapps an http request library '''
    self.http = pycurl
    self.base_url = baseurl
    self.response = StringIO()

  def initRequest(self, endpoint=''):
    self.request = self.http.Curl()
    self.request.setopt(self.http.URL, self.base_url + endpoint)
    self.request.setopt(self.http.WRITEFUNCTION, self.response.write)

  def perform(self):
    self.request.perform()
    self.request.close()
  
  def get(self, endpoint=''):
    self.initRequest(endpoint)
    self.perform()
    return self.response

  def post(self, endpoint='', data={}):
    data = urlencode(data)
    self.initRequest(endpoint)
    self.request.setopt(self.http.POST, True)
    self.request.setopt(self.http.POSTFIELDS, data)
    self.request.setopt(self.http.VERBOSE, True)
    self.perform()
    return self.response.getvalue()
