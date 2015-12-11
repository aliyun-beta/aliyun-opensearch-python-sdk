# coding=utf-8
import time
from opensearch import const
from opensearch import Client
from opensearch import IndexDoc
from opensearch import Search

try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'

app_key = ''
app_secret = ''
base_url = 'http://opensearch-cn-hangzhou.aliyuncs.com'
index_name = 'build_test_index_py27'

doc_id = 100
table_name = 'main'


def doc_add():
    # client = Client(app_key, app_secret, base_url)
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    doc = {}
    doc['id'] = doc_id
    doc['owner_id'] = 1
    doc['catalog_id'] = [12, 34]
    doc['title'] = u"this is a test title"
    doc['text'] = u"this is a test title OpenSearch"
    doc['updated'] = 1439514278
    doc['created'] = 1439514278
    ret = indexDoc.add(doc, table_name)
    time.sleep(2)
    print('add doc status: ', ret['status'])


def doc_get():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.get(doc_id, table_name)
    print("doc title: ", ret['result']['title'])


def doc_update():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    doc = {"id": doc_id, "title": "this is a test title [modify]", "text": "this is a test title [modify] OpenSearch"}
    ret = indexDoc.add(doc, table_name)
    time.sleep(2)
    print('update doc status: ', ret['status'])


def doc_after_update_get():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.get(doc_id, table_name)
    print("doc title: ", ret['result']['title'])


def search():
    client = Client(app_key, app_secret, base_url, lib=client_name)
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


def doc_delete():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.delete(doc_id, table_name)
    print('delete doc status: ', ret['status'])


if __name__ == '__main__':
    doc_add()
    doc_get()
    doc_update()
    doc_after_update_get()
    search()
    doc_delete()
