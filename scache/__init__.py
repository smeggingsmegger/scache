try:
    import simplejson as json
except ImportError:
    import json

try:
    import pandas as pd
except ImportError:
    pd = None

import csv
import os


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def index_to_letters(n):
    m = n + 1
    return colnum_string(m)


def col_to_index(name):
    pow = 1
    col_num = 0
    for letter in name[::-1]:
        col_num += (int(letter, 36) -9) * pow
        pow *= 26
    return col_num - 1


def colname_to_cell(name, row_num, the_list):
    idx = the_list.index(name)
    return '{}{}'.format(index_to_letters(idx), row_num)


class SCache():
    def __init__(self, path='./data/', debug=False):
        self.path = path
        self.debug = debug
        if not os.path.exists(path):
            os.makedirs(path)

    def _get_path(self, key, ext='json'):
        path = '{}{}.{}'.format(self.path, key, ext)
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
                value.to_json(path)
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
                value.to_csv(path, index=False)
            else:
                with open(path, 'w') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerows(value)
        else:
            print("Unsupported file type.")


    def get(self, key, fallback=dict(), ext='json', as_pandas=False, **kwargs):
        path = self._get_path(key, ext=ext)
        value = fallback
        na_filter = kwargs.get('na_filter', True)
        if as_pandas:
            if pd:
                if self.exists(key, ext=ext):
                    if ext == 'json':
                        value = pd.read_json(path, na_filter=na_filter)
                    elif ext == 'csv':
                        value = pd.read_csv(path, na_filter=na_filter)
                    else:
                        with open(path) as csvfile:
                            value = []
                            reader = csv.reader(csvfile, delimiter=',')
                            for row in reader:
                                value.append(row)

                else:
                    if self.debug:
                        print("Couldn't get value.")
            else:
                print("Pandas is not installed.")
        else:
            if self.exists(key, ext=ext):
                if ext == 'json':
                    with open(path, 'r') as f:
                        _value = f.read()
                        value = json.loads(_value)
                else:
                    with open(path) as csvfile:
                        value = []
                        reader = csv.reader(csvfile, delimiter=',')
                        for row in reader:
                            value.append(row)

            else:
                if self.debug:
                    print("Couldn't get value.")

        return value

# def _get_sc(**kwargs):
#     path = kwargs.get('path')
#     sc = SCache(path=path)
#     return sc

# def get(*args, **kwargs):
#     kwargs.pop('path')
#     sc = _get_sc(*args, **kwargs)
#     sc.get(*args, **kwargs)

# def set(*args, **kwargs):
#     kwargs.pop('path')
#     sc = _get_sc(*args, **kwargs)
#     sc.get(*args, **kwargs)
