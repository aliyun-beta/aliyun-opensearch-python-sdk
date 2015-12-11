# coding=utf-8
import time
import asyncio
from opensearch import const
from opensearch import Client
from opensearch import IndexDoc
from opensearch import Search


app_key = ''
app_secret = ''
base_url = 'http://opensearch-cn-hangzhou.aliyuncs.com'
index_name = 'build_test_index_py27'

doc_id = 1000
table_name = 'main'


@asyncio.coroutine
def doc_add():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    doc = {}
    doc['id'] = doc_id
    doc['owner_id'] = 1
    doc['catalog_id'] = [12, 34]
    doc['title'] = u"this is a test title"
    doc['text'] = u"this is a test title OpenSearch"
    doc['updated'] = 1439514278
    doc['created'] = 1439514278
    ret = yield from indexDoc.add(doc, table_name)
    client.session.close()
    time.sleep(5)
    print('add doc status: ', ret['status'])


@asyncio.coroutine
def doc_get():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = yield from indexDoc.get(doc_id, table_name)
    client.session.close()
    print("doc title: ", ret['result']['title'])


@asyncio.coroutine
def doc_update():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    doc = {"id": doc_id, "title": "this is a test title [modify]", "text": "this is a test title [modify] OpenSearch"}
    ret = yield from indexDoc.add(doc, table_name)
    client.session.close()
    time.sleep(5)
    print('update doc status: ', ret['status'])


@asyncio.coroutine
def doc_after_update_get():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = yield from indexDoc.get(doc_id, table_name)
    client.session.close()
    print("doc title: ", ret['result']['title'])


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


@asyncio.coroutine
def doc_delete():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = yield from indexDoc.delete(doc_id, table_name)
    client.session.close()
    print('delete doc status: ', ret['status'])


@asyncio.coroutine
def run():
    yield from doc_add()
    yield from doc_get()
    yield from doc_update()
    yield from doc_after_update_get()
    yield from search()
    yield from doc_delete()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
