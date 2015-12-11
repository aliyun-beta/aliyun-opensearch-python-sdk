# coding=utf-8

import time
import pytest
from opensearch import Client
from opensearch import IndexApp
from config import app_key, app_secret, base_url, index_name


@pytest.mark.asyncio
def test_create():
    client = Client(app_key, app_secret, base_url)
    indexApp = IndexApp(client)
    ret = yield from indexApp.create(index_name, 'tpl_test')
    client.session.close()
    assert ret['status'] == 'OK'
    time.sleep(5)


@pytest.mark.asyncio
def test_getAll():
    client = Client(app_key, app_secret, base_url)
    indexApp = IndexApp(client)
    ret = yield from indexApp.getAll()
    print(ret)
    client.session.close()
    assert ret['status'] == 'OK'
    print(ret['result'])


@pytest.mark.asyncio
def test_status():
    client = Client(app_key, app_secret, base_url)
    indexApp = IndexApp(client)
    ret = yield from indexApp.status(index_name)
    client.session.close()
    assert ret['status'] == 'OK'
    print(ret['result'])


@pytest.mark.asyncio
def test_delete():
    client = Client(app_key, app_secret, base_url)
    indexApp = IndexApp(client)
    ret = yield from indexApp.delete(index_name)
    client.session.close()
    assert ret['status'] == 'OK'
