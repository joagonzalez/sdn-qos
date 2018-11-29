# python ticker
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
   ''' tu codigo va a terminar a los 200 segundos que se termine el ticker '''
   timeTicker(timeTrafficEmulationCallback, 200)
   # aca ya no pasa nada y se corta el programa

if __name__ == '__main__':
  main()