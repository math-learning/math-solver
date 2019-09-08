import os

class Environment:
    
    @staticmethod
    def is_production() -> bool :
        return os.environ.get('ENV') == 'PROD'
