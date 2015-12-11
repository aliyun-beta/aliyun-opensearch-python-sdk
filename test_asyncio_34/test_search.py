# coding=utf-8

import pytest
from opensearch import const
from opensearch import Client
from opensearch import IndexApp
from opensearch import Search
from opensearch import Suggest
from config import app_key, app_secret, base_url, build_index_name

table_name = 'main'
index_name = build_index_name


@pytest.mark.asyncio
def test_search():
    client = Client(app_key, app_secret, base_url)
    indexSearch = Search(client)
    indexSearch.addIndex(index_name)
    indexSearch.addSort('updated', const.SEARCH_SORT_DESC)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.query = "default:'opensearch'"
    indexSearch.addAggregate('created', 'count()')
    # indexSearch.addDistinct('owner_id')
    indexSearch.start = 0
    indexSearch.hits = 50
    ret = yield from indexSearch.call()
    print(ret)
    client.session.close()
    assert ret['status'] == 'OK'


@pytest.mark.asyncio
def test_scroll():
    client = Client(app_key, app_secret, base_url)
    indexSearch = Search(client)
    indexSearch.addIndex(index_name)
    # indexSearch.addSort('updated', const.SEARCH_SORT_DESC)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.query = "default:'opensearch'"
    indexSearch.addAggregate('created', 'count()')
    # indexSearch.addDistinct('owner_id')
    indexSearch.start = 0
    indexSearch.hits = 50
    ret = yield from indexSearch.scroll('1m', search_type='scan')
    print(ret)
    client.session.close()
    assert ret['status'] == 'OK'


@pytest.mark.asyncio
def test_suggest():
    client = Client(app_key, app_secret, base_url)
    suggest = Suggest(client, index_name)
    ret = yield from suggest.call('open', 'test_suggest', hit=10)
    print(ret)
    client.session.close()
    assert len(ret['suggestions']) > 0
