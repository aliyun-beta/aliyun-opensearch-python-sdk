# coding=utf-8

import time
from opensearch import Client
from opensearch import IndexApp
from .config import app_key, app_secret, base_url, index_name, client_name


def test_create():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.create(index_name, 'tpl_test')
    print(ret)
    assert ret['status'] == 'OK'


def test_get_all():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.getAll()
    print(ret)
    assert ret['status'] == 'OK'
    print(ret['result'])


def test_get_all_page():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.getAll(page=1, size=50)
    print(ret)
    assert ret['status'] == 'OK'
    print(ret['result'])


def test_status():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.status(index_name)
    assert ret['status'] == 'OK'
    print(ret['result'])


def test_delete():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.delete(index_name)
    assert ret['status'] == 'OK'
