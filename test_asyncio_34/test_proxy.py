# coding=utf-8
import pytest
from opensearch import const
from opensearch import Client
from opensearch import ErrorLog
from config import app_key, app_secret, base_url, build_index_name

proxy = 'http://proxy.xxx.com'
index_name = build_index_name


@pytest.mark.asyncio
def test_errlog():
    client = Client(app_key, app_secret, base_url, proxy=proxy)
    errLog = ErrorLog(client, index_name)
    ret = yield from errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC)
    print(ret)
    client.session.close()
    assert ret['status'] == 'OK'


@pytest.mark.asyncio
def test_errlog_post():
    client = Client(app_key, app_secret, base_url, proxy=proxy)
    errLog = ErrorLog(client, index_name)
    ret = yield from errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC, method=const.HTTP_POST)
    print(ret)
    client.session.close()
    assert ret['status'] == 'OK'
