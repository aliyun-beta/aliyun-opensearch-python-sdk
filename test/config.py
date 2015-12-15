# coding=utf-8
import os
import uuid

app_key = os.environ.get('ALIYUN_OPENSEARCH_KEY')
app_secret = os.environ.get('ALIYUN_OPENSEARCH_SECRET')
base_url = 'http://opensearch-cn-hangzhou.aliyuncs.com'
index_name = 't_' + str(uuid.uuid4()).replace('-', '')[2:30]
build_index_name = 'build_test_index_py27'

try:
    import requests
    client_name = 'requests'
except ImportError:
    client_name = 'httplib'
