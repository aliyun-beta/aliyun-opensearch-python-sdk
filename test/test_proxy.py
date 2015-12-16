# coding=utf-8
import os
from opensearch import const
from opensearch import Client
from opensearch import ErrorLog
from config import app_key, app_secret, base_url, build_index_name, client_name

proxy = os.environ.get('ALIYUN_HTTP_PROXY')
index_name = build_index_name


def test_errlog():
    client = Client(app_key, app_secret, base_url, lib='httplib', proxy=proxy)
    errLog = ErrorLog(client, index_name)
    ret = errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC)
    print(ret)
    assert ret['status'] == 'OK'


def test_errlog_post():
    client = Client(app_key, app_secret, base_url, lib=client_name, proxy=proxy)
    errLog = ErrorLog(client, index_name)
    ret = errLog.call(1, 50, sort_mode=const.LOG_SORT_ASC, method=const.HTTP_POST)
    print(ret)
    assert ret['status'] == 'OK'
