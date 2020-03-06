[![](https://img.shields.io/pypi/pyversions/scache.svg?longCache=True)](https://pypi.org/project/scache/)
[![](https://img.shields.io/pypi/v/scache.svg?maxAge=3600)](https://pypi.org/project/scache/)
[![Travis](https://api.travis-ci.org/smeggingsmegger/scache.py.svg?branch=master)](https://travis-ci.org/smeggingsmegger/scache.py/)

# Python Simple Cache - scache

##

#### Installation
```bash
$ [sudo] pip install scache
```

#### How it works
scache uses .json files in the data subdirectory by default. If they exist, they are overwritten. If they do not, they are created.

`./data/<key>.json` by default

#### Get Started
```python
'''Optional parameters:
path: (string) Path where to store the .json cache data.
    defaults to './data/'
debug: (boolean) Prints debug information such as whether or not keys were found.
    defaults to False
'''
from scache import SCache
scache = SCache()
scache.set('key', 'value')
```

#### Functions
function|`__doc__`
-|-
`scache.get(key)` | Gets cache value.
`scache.get(key, value)` | Sets cache value.
`scache.get(key, default)` | Get cache value. Return default if not found
`scache.rm(key)` | Remove cache by key
`scache.exists(key)` | returns True if key exists, else returns False
`scache.empty()` | Clears the entire cache.

#### Examples
```python
>>> import scache
>>> scache.set("key", {'test': 1})
>>> scache.get("key")
"{'test': 1}"
>>> scache.exists("key")
True
>>> scache.rm("key")
>>> scache.empty() # clears entire cache
```
