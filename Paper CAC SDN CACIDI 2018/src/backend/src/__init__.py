__version__ = '0.1'

from .cac.Application import Application
from .front.Facade import FacadeWsService

# Setup application
def run():
  Cac = Application()
  Cac.run()

  if Cac.listen:
    FacadeApp = FacadeWsService()
    FacadeApp.register_command(Cac.getMetrics, 'getMetrics')
    FacadeApp.register_command(Cac.getPorts, 'getPorts')
    FacadeApp.run()
