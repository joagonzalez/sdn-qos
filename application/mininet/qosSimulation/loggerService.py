import logging

class LoggerService:
    '''
    Logging Wrapper 
    '''
    def __init__(self):
        self.loggerService = self.createLogger()

    def createLogger(self):
         logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - %(process)s - %(message)s')
         logger = logging.getLogger( __name__ )
         return logger

    def getLogger(self):
        return self.logger

    def debug(self, message):
        return self.loggerService.debug(message)

    def info(self, message):
       return self.loggerService.info(message)

    def warning(self, message):
       return self.loggerService.warning(message)

    def error(self, message):
       return self.loggerService.error(message)

loggerService = LoggerService()