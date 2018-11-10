from os import path
import logging
import logging.config

logConfigFile = path.join(path.dirname(path.abspath(__file__)), 'logger.ini')
logging.config.fileConfig( logConfigFile )

''' Good practices with Logger python '''
''' https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/ '''