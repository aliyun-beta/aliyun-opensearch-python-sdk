# coding=utf-8
import uuid

app_key = ''
app_secret = ''
base_url = 'http://opensearch-cn-hangzhou.aliyuncs.com'
index_name = 't_' + str(uuid.uuid4()).replace('-', '')[2:30]
build_index_name = 'build_test_index_py27'
