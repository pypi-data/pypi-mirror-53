<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/kv-cache.svg?longCache=True)](https://pypi.org/project/kv-cache/)

#### Installation
```bash
$ [sudo] pip install kv-cache
```

#### How it works
```
$KV_CACHE/<key>
```

`$XDG_CACHE_HOME/kv-value/<key>` by default

#### Functions
function|`__doc__`
-|-
`kv_cache.exists(key)` |return True if key exists, else False
`kv_cache.get(key)` |get cache value
`kv_cache.rm(key)` |remove cache key
`kv_cache.update(key, string)` |update cache value

#### Examples
```python
>>> import kv_cache
>>> kv_cache.update("key",'value')
>>> kv_cache.get("key")
'value'
>>> kv_cache.exists("key")
True
>>> kv_cache.rm("key")
>>> kv_cache.clear() # clear all keys
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>