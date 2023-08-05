<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/requests-etag-cache.svg?longCache=True)](https://pypi.org/project/requests-etag-cache/)

#### Installation
```bash
$ [sudo] pip install requests-etag-cache
```

#### How it works
```
$REQUESTS_ETAG_CACHE/<url_hash>
```

`$XDG_CACHE_HOME/requests-etag-cache/<url_hash>` by default

#### Functions
function|`__doc__`
-|-
`requests_etag_cache.clear()` |remove all cache keys
`requests_etag_cache.get(response)` |get cached etag value
`requests_etag_cache.rm(response)` |remove response cache
`requests_etag_cache.save(response)` |save response etag value
`requests_etag_cache.uptodate(response)` |return True if response is cached, else False

#### Examples
```python
import requests
import requests_etag_cache

r = requests.get('https://pypi.org/project/requests/')
if not requests_etag_cache.uptodate(r):
    ...
    requests_etag_cache.save(r)
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>