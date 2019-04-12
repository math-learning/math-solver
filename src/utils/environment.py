import os

class Environment:
    
    @staticmethod
    def is_production():
        return os.environ.get('ENV') != 'LOCAL'
