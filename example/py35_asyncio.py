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


async def doc_add():
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
    ret = await indexDoc.add(doc, table_name)
    client.session.close()
    time.sleep(5)
    print('add doc status: ', ret['status'])


async def doc_get():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = await indexDoc.get(doc_id, table_name)
    client.session.close()
    print("doc title: ", ret['result']['title'])


async def doc_update():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    doc = {"id": doc_id, "title": "this is a test title [modify]", "text": "this is a test title [modify] OpenSearch"}
    ret = await indexDoc.add(doc, table_name)
    client.session.close()
    time.sleep(5)
    print('update doc status: ', ret['status'])


async def doc_after_update_get():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = await indexDoc.get(doc_id, table_name)
    client.session.close()
    print("doc title: ", ret['result']['title'])


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


async def doc_delete():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = await indexDoc.delete(doc_id, table_name)
    client.session.close()
    print('delete doc status: ', ret['status'])


async def run():
    await doc_add()
    await doc_get()
    await doc_update()
    await doc_after_update_get()
    await search()
    await doc_delete()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
