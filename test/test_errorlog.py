# coding=utf-8
import pytest
from opensearch import const
from opensearch import Client
from opensearch import ErrorLog
from config import app_key, app_secret, base_url, build_index_name, client_name

index_name = build_index_name


def test_errlog():
    client = Client(app_key, app_secret, base_url, lib='httplib')
    errLog = ErrorLog(client, index_name)
    ret = errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC)
    print(ret)
    assert ret['status'] == 'OK'


def test_errlog_post():
    client = Client(app_key, app_secret, base_url, lib='httplib')
    errLog = ErrorLog(client, index_name)
    ret = errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC, method=const.HTTP_POST)
    print(ret)
    assert ret['status'] == 'OK'


def test_errlog_raise():
    with pytest.raises(const.ArgError):
        client = Client(app_key, app_secret, base_url, lib='httplib')
        errLog = ErrorLog(client, index_name)
        errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC, method='PUT')


def test_errlog_raise2():
    with pytest.raises(const.ArgError):
        client = Client(app_key, app_secret, base_url, lib=client_name)
        errLog = ErrorLog(client, index_name)
        errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC, method='PUT')
