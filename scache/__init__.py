try:
    import simplejson as json
except ImportError:
    import json

try:
    import pandas as pd
except ImportError:
    pd = None

import os


class SCache():
    def __init__(self, path='./data/', debug=False):
        self.path = path
        self.debug = debug
        if not os.path.exists(path):
            os.makedirs(path)

    def _get_path(self, key, ext='json'):
        path = '{}{}.{}'.format(self.path, key, ext)
        print(path)
        return path
    
    def clear(self):
        for file_name in os.listdir(self.path):
            if file_name.endswith('.json') or file_name.endswith('.csv'):
                os.remove(self.path + file_name)

    def rm(self, key, ext='json'):
        path = self._get_path(key, ext=ext)
        if self.exists(key):
            os.remove(path)
        else:
            if self.debug:
                print("Key: {} does not exist".format(key))

    def exists(self, key, ext='json'):
        path = self._get_path(key, ext=ext)
        exst = os.path.exists(path)
        return exst
        
    def set(self, key, value, pprint=True, as_type='json'):
        if as_type == 'json':
            path = self._get_path(key, ext='json')
            if str(type(value)) == "<class 'pandas.core.frame.DataFrame'>":
                value.to_json(path, orient='split')
            else:
                with open(path, 'w+') as f:
                    if pprint:
                        f.write(json.dumps(value, sort_keys=True, indent=4, separators=(',', ': ')))
                    else:
                        f.write(json.dumps(value))
        elif as_type == 'csv':
            path = self._get_path(key, ext='csv')
            if str(type(value)) == "<class 'pandas.core.frame.DataFrame'>":
                # Dump with pandas
                value.to_csv(path, orient='split')
            else:
                print("Not implemented.")
        else:
            print("Unsupported file type.")


    def get(self, key, fallback=dict(), ext='json', as_pandas=False):
        path = self._get_path(key, ext=ext)
        value = fallback
        if as_pandas:
            if pd:
                if self.exists(key, ext=ext):
                    if ext == 'json':
                        value = pd.read_json(path)
                    elif ext == 'csv':
                        value = pd.read_csv(path)
                    else:
                        print("Not implemented.")
                else:
                    if self.debug:
                        print("Couldn't get value.")
            else:
                print("Pandas is not installed.")
        else:
            if self.exists(key, ext=ext):
                with open(path, 'r') as f:
                    _value = f.read()
                    value = json.loads(_value)
            else:
                if self.debug:
                    print("Couldn't get value.")

        return value
