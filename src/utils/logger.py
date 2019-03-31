import logging

class Logger:
    @staticmethod
    def getLogger():
        return logging.getLogger("flask.app")
