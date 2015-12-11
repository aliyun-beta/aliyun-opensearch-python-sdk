# coding=utf-8

import time
import pytest
from opensearch import Client
from opensearch import IndexApp
from opensearch import IndexDoc
from config import app_key, app_secret, base_url, index_name

doc_id = 1
table_name = 'main'


@pytest.mark.asyncio
def test_create():
    client = Client(app_key, app_secret, base_url)
    indexApp = IndexApp(client)
    ret = yield from indexApp.create(index_name, 'tpl_test')
    client.session.close()
    assert ret['status'] == 'OK'
    time.sleep(5)


@pytest.mark.asyncio
def test_add():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    doc = {"id": doc_id, "title": u"这是一个测试标题", "text": u"这是一个测试标题 OpenSearch", "updated": 1439514278, "created": 1439514278}
    ret = yield from indexDoc.add(doc, table_name)
    client.session.close()
    assert ret['status'] == 'OK'
    time.sleep(5)


@pytest.mark.asyncio
def test_get():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = yield from indexDoc.get(doc_id, table_name)
    client.session.close()
    print(ret)
    assert ret['status'] == 'OK'


@pytest.mark.asyncio
def test_update():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    doc = {"id": doc_id, "title": "这是一个测试标题的[修改]", "text": "这是一个测试标题的修改 OpenSearch"}
    ret = yield from indexDoc.add(doc, table_name)
    client.session.close()
    assert ret['status'] == 'OK'
    time.sleep(5)


@pytest.mark.asyncio
def test_after_update_get():
    client = Client(app_key, app_secret, base_url)
    indexDoc = IndexDoc(client, index_name)
    ret = yield from indexDoc.get(doc_id, table_name)
    client.session.close()
    print(ret)
    assert ret['status'] == 'OK'


@pytest.mark.asyncio
def test_app_delete():
    client = Client(app_key, app_secret, base_url)
    indexApp = IndexApp(client)
    ret = yield from indexApp.delete(index_name)
    client.session.close()
    assert ret['status'] == 'OK'
