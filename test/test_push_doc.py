# coding=utf-8

import time
from opensearch import Client
from opensearch import IndexApp
from opensearch import IndexDoc
from config import app_key, app_secret, base_url, build_index_name, client_name

doc_id = 1
table_name = 'main'
index_name = build_index_name


def test_push_add():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    status = indexDoc.pushCSVFile('add', './test/test.csv', table_name, 0, 'id', multi_fields=['catalog_id'])
    print(status)
    assert status == 'OK'
    time.sleep(5)


def test_push_add2():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    status = indexDoc.pushCSVFile('add', './test/test2.csv', table_name, 0, 'id', multi_fields=['catalog_id'], max_size=100)
    print(status)
    assert status == 'OK'
    time.sleep(5)


def test_push_update():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    status = indexDoc.pushCSVFile('update', './test/test.csv', table_name, 0, 'id', multi_fields=['catalog_id'])
    print(status)
    assert status == 'OK'
    time.sleep(5)


def test_push_update2():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    status = indexDoc.pushCSVFile('update', './test/test2.csv', table_name, 0, 'id', multi_fields=['catalog_id'], max_size=100)
    print(status)
    assert status == 'OK'
    time.sleep(5)


def test_deletes():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.delete([100, 101, 102, 103, 200, 201, 202, 203], table_name)
    assert ret['status'] == 'OK'
    time.sleep(5)
