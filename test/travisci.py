# coding=utf-8

from opensearch import const
from opensearch import Client
from opensearch import IndexApp
from opensearch import Search
from opensearch import Suggest
from config import app_key, app_secret, base_url, build_index_name, client_name

table_name = 'main'
index_name = build_index_name


def test_search():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexSearch = Search(client)
    indexSearch.addIndex(index_name)
    indexSearch.addSort('updated', const.SEARCH_SORT_DESC)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.query = "default:'opensearch'"
    agg_range = ['0~1439514378', '1439514378~1539514378']
    indexSearch.addAggregate('created', 'count()', agg_sampler_threshold=10000, agg_sampler_step=5,
                             agg_filter="created>1423456781", max_group=100, agg_range=agg_range)
    grade = [3.0, 5.0]
    indexSearch.addDistinct('owner_id', grade=grade)
    indexSearch.addFilter('owner_id>=1')
    indexSearch.addFilter('created>=1439514200')
    indexSearch.addSummary("text", length=100, element='em', ellipsis='...',
                           snipped=1, element_prefix='<em>', element_postfix='</em>')
    indexSearch.qp = 'stop_word'
    indexSearch.disable = 'qp'
    indexSearch.start = 0
    indexSearch.hits = 50
    indexSearch.format = 'json'
    indexSearch.rerank_size = 200
    indexSearch.formula_name = 'default'
    indexSearch.first_formula_name = 'default'
    indexSearch.kvpairs = 'duniqfield:owner_id'
    ret = indexSearch.call()
    print('test_search', ret)
    assert ret['status'] == 'OK'


def test_scroll():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexSearch = Search(client)
    indexSearch.addIndex(index_name)
    indexSearch.fetch_fields = ['id', 'title', 'updated']
    indexSearch.query = "default:'opensearch'"
    indexSearch.addFilter('owner_id>=1')
    indexSearch.formula_name = 'default'
    indexSearch.first_formula_name = 'default'
    indexSearch.addSummary("text", length=100, element='em', ellipsis='...',
                           snipped=1, element_prefix='<em>', element_postfix='</em>')
    indexSearch.qp = 'stop_word'
    indexSearch.disable = 'qp'
    ret = indexSearch.scroll('1m', search_type='scan')
    print(ret)
    assert ret['status'] == 'OK'


def test_suggest():
    '''
        must had set suggest rule name "test_suggest"
    '''
    client = Client(app_key, app_secret, base_url, lib=client_name)
    suggest = Suggest(client, index_name)
    ret = suggest.call('open', 'test_suggest', hit=10)
    print(ret)
    assert len(ret['suggestions']) >= 0
