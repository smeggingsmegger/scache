try:
    import simplejson as json
except ImportError:
    import json

import os


class SCache():
    def __init__(self, path='./data/', debug=False):
        self.path = path
        self.debug = debug
        if not os.path.exists(path):
            os.makedirs(path)

    def _get_path(self, key):
        return '{}{}.json'.format(self.path, key)
    
    def clear(self):
        for file_name in os.listdir(self.path):
            if file_name.endswith('.json'):
                os.remove(self.path + file_name)

    def rm(self, key):
        path = self._get_path(key)
        if self.exists(key):
            os.remove(path)
        else:
            if self.debug:
                print("Key: {} does not exist".format(key))

    def exists(self, key):
        path = self._get_path(key)
        return os.path.exists(path)
        
    def set(self, key, value, pprint=True):
        path = self._get_path(key)
        with open(path, 'w+') as f:
            if pprint:
                f.write(json.dumps(value, sort_keys=True, indent=4, separators=(',', ': ')))
            else:
                f.write(json.dumps(value))


    def get(self, key, fallback=dict()):
        path = self._get_path(key)
        value = fallback
        if self.exists(key):
            with open(path, 'r') as f:
                _value = f.read()
                value = json.loads(_value)
        else:
            if self.debug:
                print("Couldn't get value.")

        return value
