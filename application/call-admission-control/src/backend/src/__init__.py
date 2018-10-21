__version__ = '0.1'

from .config import logger
from .cac.Application import Application
from .front.Facade import FacadeWsService
from .front.Client import Client

# Setup application
def run():
  frontClient = Client()
  Cac = Application(frontClient)
  Cac.run()

  if Cac.listen:
    FacadeApp = FacadeWsService() # Renombrar el nombre de FAcade por dió!
    FacadeApp.register_command(Cac.getMetrics, 'getMetrics')
    FacadeApp.register_command(Cac.getPorts, 'getPorts')
    FacadeApp.run(frontClient)
