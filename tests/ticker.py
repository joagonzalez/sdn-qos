# python ticker
from threading import Thread
from time import sleep

def trafficEmulatorHandler(params):
  ''' este es el que hace algo con los hosts.. nose cambias el trafico
      recibis los hosts por parametros se los podrias pasar nose '''
  print('hola!')

timeTrafficEmulationMap = {
   5: {
     "handler": trafficEmulatorHandler, # callback handler puede ser cualquiera
     "params": [] # parametros para el handler de los 5 segundos
   },
   10: {
     "handler": trafficEmulatorHandler, # callback handler puede ser cualquiera
     "params": [] # parametros para el handler de los 10 segundos
   },
   # n things.. happend until finishTime
}

def timeTrafficEmulationCallback(time):
   ''' Esta funcion es la que llama al mapa si el momento del tiempo esta
       definido en tu emulacion '''
   if (time in timeTrafficEmulationMap):
     # fijate que agarro el handler del Map y la ejecuto con los parametros del Map tambien
    timeTrafficEmulationMap[time]['handler'](
      params=timeTrafficEmulationMap[time]['params']
    )

def timeTicker(callback, timeFinish):
  timeTicker = 1 # empieza en el segundo 1
  while(timeTicker < timeFinish):
    print "second {}".format(timeTicker)
    sleep(1) # dormis 1 segundo
    callback(timeTicker) # se ejecuta cada 1 segundo tu funcion
    timeTicker += 1 # sumas de a 1 segundo

def main():
   ''' aca esta el codigo de tu iperf, proceso principal
       y cuando queres empezar a ejecutar tu simulacion en tiempo real..
       creas un thread nuevo que no te ocupe tu proceso principal
       le podes pasar como parametros el callback que queres que ejecute '''
   nodeHandler = Thread(
     target=timeTicker,
     kwargs={
       "callback": timeTrafficEmulationCallback,
       "timeFinish": 200 # segundos
     }
   )
   nodeHandler.daemon=True
   nodeHandler.start()
   ''' aca hago que mi main dure 40 segundos la aplicacion entera..
       pero tu app al quedar escuchando o generando cosas
       va a durar lo q tenga q durar '''
   sleep(40)

if __name__ == '__main__':
  main()