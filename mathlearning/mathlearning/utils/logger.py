import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from mathlearning.utils.environment import Environment

LOGGING_FILE = 'log.log'
FORMATTER_STYLE = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LEVEL = logging.INFO


class Logger:
    __initialized = False

    @classmethod
    def getLogger(clazz):
        logger = logging.getLogger("flask.app")
        if not clazz.__initialized and Environment.is_production():
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            logger.setLevel(logging.INFO)
            # time_handler = TimedRotatingFileHandler(LOGGING_FILE,
            #                            when="m",
            #                            interval=1,
            #                            backupCount=5)

            # time_handler.setFormatter(formatter)
            # logger.addHandler(time_handler)

            clazz.__initialized = True

        return logger
