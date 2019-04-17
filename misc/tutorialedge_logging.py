import logging
import logging.handlers as handlers
import time

## FORMATTING LOG STATEMENTS
# This allows you to capture process/thread names with every log statement without having to explicitly state them within the
# message you are logging

## ROLLING LOG FILES
# In the logging module there are both RotatingFileHandler and TimedRotatingFileHandler classes

# A rotating file handler allows us to rotate our log statements into a new file every time our log file reaches a certain size

logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

# Initialize formatter 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler('logs/timed_app.log', when='M', interval=1, backupCount=0) 
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

errorlogHandler = handlers.RotatingFileHandler('logs/error_log.log', maxBytes=5000, backupCount=0)
errorlogHandler.setLevel(logging.ERROR)
errorlogHandler.setFormatter(formatter)
logger.addHandler(errorlogHandler)

def main():
    while True:
        time.sleep(1)
        logger.info('A Sample Log Statement')

main()
