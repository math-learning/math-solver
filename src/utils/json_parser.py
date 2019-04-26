import json

class ComplexEncoder(json.JSONEncoder):
     def default(self, obj):
         if hasattr(obj, 'to_json'):
             return obj.to_json()
         return json.JSONEncoder.default(self, obj)

class JsonParser:

    @staticmethod
    def dumps(object):
        return  json.dumps(object, cls=ComplexEncoder)
        
    @staticmethod
    def dumps_pretty( object):
        return  json.dumps(object, cls=ComplexEncoder, 
            sort_keys=True, indent=4) 