# Aliyun OpenSearch

this is a Aliyun opensearch python SDK library. 

## Installation

This package can be installed through this way.

``` bash
python setup.py install
```

## Feature

* default does not dependent third-party packages
  
* compatible python 2.7, python 3.x
  
* support http proxy call api.
  
* supports csv file batch push and have a push log record. If interrupted, you can pushCSVFile function's offset parameter, continue to push.
  
* http client library supports standard library httplib, [requests](https://github.com/kennethreitz/requests) and [aiohttp](https://github.com/KeepSafe/aiohttp/). will be automatically adapted according to your environment. aiohttp only apply to python 3.x. 
  
* installed aiohttp,  support  python 3.4.1 (yield from) ,python 3.5 (async/await) Coroutine asynchronous non-blocking.
  
* If you installed the ujson, it will use this toolkit, if not using the default standard library. ujson is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 2.5+ and 3. Recommended Use ujson.
  
  ​
  
  ​

## Test Suite

``` python
pip install pytest
pip install pytest-cov
```

If the environment is python 3.x asyncio

``` python
pip install pytest-asyncio
```



``` 
(opensearch27_requests)jin$ py.test --cov-report term-missing --cov=opensearch test/
platform darwin -- Python 2.7.10, pytest-2.8.2, py-1.4.30, pluggy-0.3.1
rootdir: /Users/jin/Project/aliyun/OpenSearch, inifile: 
plugins: cov-2.2.0
collected 26 items 

test/test_app.py .....
test/test_const.py ...
test/test_document.py .........
test/test_errorlog.py ..
test/test_push_doc.py ...
test/test_search.py ....
----------------- coverage: platform darwin, python 2.7.10-final-0 -----------------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
opensearch/__init__.py       7      0   100%   
opensearch/app.py           32      1    97%   39
opensearch/client.py       108     14    87%   16-17, 32-33, 38-42, 48, 103, 126, 148, 166
opensearch/const.py         13      0   100%   
opensearch/document.py      79      9    89%   55, 101, 104, 118-121, 129-132
opensearch/errorlog.py      14      0   100%   
opensearch/search.py       166      4    98%   58, 66, 97, 214
opensearch/suggest.py       13      0   100%   
------------------------------------------------------
TOTAL                      432     28    94%   
```



## Usage

##### Example

``` python
def search():
    client = Client(app_key, app_secret, base_url)
    indexSearch = Search(client)
    indexSearch.query = "default:'opensearch'"
    indexSearch.addIndex(index_name)
    indexSearch.addSort('updated', const.SEARCH_SORT_DESC)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.addAggregate('created', 'count()')
    indexSearch.addDistinct('owner_id')
    indexSearch.start = 0
    indexSearch.hits = 50
    ret = indexSearch.call()
    print('search result: ', ret)
```

##### python 3.4.1 asyncio Example

``` python
@asyncio.coroutine
def search():
    client = Client(app_key, app_secret, base_url)
    indexSearch = Search(client)
    indexSearch.query = "default:'opensearch'"
    indexSearch.addIndex(index_name)
    indexSearch.addSort('updated', const.SEARCH_SORT_DESC)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.addAggregate('created', 'count()')
    indexSearch.addDistinct('owner_id')
    indexSearch.start = 0
    indexSearch.hits = 50
    ret = yield from indexSearch.call()
    client.session.close()
    print('search result: ', ret)
```

##### python 3.5 asyncio Example

``` python
async def search():
    client = Client(app_key, app_secret, base_url)
    indexSearch = Search(client)
    indexSearch.query = "default:'opensearch'"
    indexSearch.addIndex(index_name)
    indexSearch.addSort('updated', const.SEARCH_SORT_DESC)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.addAggregate('created', 'count()')
    indexSearch.addDistinct('owner_id')
    indexSearch.start = 0
    indexSearch.hits = 50
    ret = await indexSearch.call()
    client.session.close()
    print('search result: ', ret)
```

more examples in the example directory



## TODO

* test support for flask, bottle and tornado web frameworks

## License