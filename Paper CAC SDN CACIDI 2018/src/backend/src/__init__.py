__version__ = '0.1'

from .cac.Application import Application
from .front.Facade import FacadeWsService

# Setup application
def run():
  Cac = Application()
  Cac.run()

  print('y aca llegaaaaaaa??')

  if Cac.listen:
    FacadeApp = FacadeWsService()
    FacadeApp.register_command(Cac.getMetrics, 'getMetrics')
    FacadeApp.run()
