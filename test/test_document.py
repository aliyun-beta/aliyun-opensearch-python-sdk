# coding=utf-8

import time
from opensearch import Client
from opensearch import IndexApp
from opensearch import IndexDoc
from config import app_key, app_secret, base_url, index_name, client_name

doc_id = 1
table_name = 'main'


def test_app_create():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.create(index_name, 'tpl_test')
    assert ret['status'] == 'OK'
    time.sleep(5)


def test_add():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    doc = {"id": doc_id, "title": u"这是一个测试标题", "text":
           u"这是一个测试标题 OpenSearch", "updated": 1439514278, "created": 1439514278}
    ret = indexDoc.add(doc, table_name)
    assert ret['status'] == 'OK'
    time.sleep(5)


def test_adds():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)

    docs = []
    item = {}
    item['id'] = 2
    item['owner_id'] = 2
    item['catalog_id'] = [11, 56]
    item['title'] = u"阿里云开源众包计划 - OpenSearch C++ SDK 开发"
    item['text'] = u"阿里云开源众包计划 - OpenSearch C++ SDK 开发 100%实现阿里云OpenSearch的C++语言SDK 需要跨Windows、Linux、MacOS三个平台"
    item['updated'] = 1439514278
    item['created'] = 1439514278
    docs.append(item)

    item = {}
    item['id'] = 3
    item['owner_id'] = 1
    item['catalog_id'] = [12, 34]
    item['title'] = u"阿里云开源众包计划 - OpenSearch Python SDK 开发"
    item['text'] = u"阿里云开源众包计划 - OpenSearch Python SDK 开发 项目结束后，开发者需要继续三个月的bug维护期"
    item['updated'] = 1439514278
    item['created'] = 1439514278
    docs.append(item)

    ret = indexDoc.add(docs, table_name)
    assert ret['status'] == 'OK'
    time.sleep(5)


def test_get():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.get(doc_id, table_name)
    print(ret)
    assert ret['status'] == 'OK'


def test_update():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    doc = {
        "id": doc_id, "title": "这是一个测试标题的[修改]", "text": "这是一个测试标题的修改 OpenSearch"}
    ret = indexDoc.add(doc, table_name)
    assert ret['status'] == 'OK'
    time.sleep(5)


def test_after_update_get():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.get(doc_id, table_name)
    print(ret)
    assert ret['status'] == 'OK'


def test_delete():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.delete(doc_id, table_name)
    assert ret['status'] == 'OK'
    time.sleep(5)


def test_deletes():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.delete([2, 3], table_name)
    assert ret['status'] == 'OK'
    time.sleep(5)


def test_app_delete():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.delete(index_name)
    assert ret['status'] == 'OK'
