# coding=utf-8
import csv
import time
from opensearch import Client
from opensearch import IndexApp
from opensearch import IndexDoc
from config import app_key, app_secret, base_url, build_index_name, client_name

table_name = 'main'
index_name = build_index_name


def create_index():
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexApp = IndexApp(client)
    ret = indexApp.create(index_name, 'tpl_test')
    assert ret['status'] == 'OK'
    time.sleep(2)

docs = []
item = {}
item['id'] = 1
item['owner_id'] = 1
item['catalog_id'] = [12, 34]
item['title'] = u"这是一个测试标题"
item['text'] = u"这是一个测试标题 OpenSearch"
item['updated'] = 1439514278
item['created'] = 1439514278
docs.append(item)


item = {}
item['id'] = 2
item['owner_id'] = 2
item['catalog_id'] = [11, 56]
item['title'] = u"阿里云开源众包计划 - OpenSearch C++ SDK 开发"
item['text'] = u"阿里云开源众包计划 - OpenSearch C++ SDK 开发 100%实现阿里云OpenSearch的C++语言SDK 需要跨Windows、Linux、MacOS三个平台"
item['updated'] = 1439514278
item['created'] = 1439514278
docs.append(item)


item = {}
item['id'] = 3
item['owner_id'] = 1
item['catalog_id'] = [12, 34]
item['title'] = u"阿里云开源众包计划 - OpenSearch Python SDK 开发"
item['text'] = u"阿里云开源众包计划 - OpenSearch Python SDK 开发 项目结束后，开发者需要继续三个月的bug维护期"
item['updated'] = 1439514278
item['created'] = 1439514278
docs.append(item)


item = {}
item['id'] = 4
item['owner_id'] = 4
item['catalog_id'] = [56, 68]
item['title'] = u"OSC招聘沙龙完美收官，四小时促成六成高端人才入职"
item['text'] = u"OSC招聘沙龙完美收官，四小时促成六成高端人才入职 11月14日，开源中国成功举办了第一届线下招聘沙龙活动（Java架构师专场）。本次活动中，筛选了 5 家报名企业，其中 3 家企业招到满意人才，甚至有一家企业招到4个人才。正如活动宣传中说的：“四小时，面试五家企业，拿到offer。”"
item['updated'] = 1439514278
item['created'] = 1439514278
docs.append(item)


def doc_add(docs):
    client = Client(app_key, app_secret, base_url, lib=client_name)
    indexDoc = IndexDoc(client, index_name)
    ret = indexDoc.add(docs, table_name)
    assert ret['status'] == 'OK'
    print(ret)
    time.sleep(10)


def csv_file():
    with open('./test/test.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['id', 'owner_id', 'catalog_id', 'title', 'text', 'updated', 'created'])
        writer.writerow([100, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])
        writer.writerow([101, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])
        writer.writerow([102, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])
        writer.writerow([103, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])


def csv_file2():
    with open('./test/test2.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['id', 'owner_id', 'catalog_id', 'title', 'text', 'updated', 'created'])
        writer.writerow([200, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])
        writer.writerow([201, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])
        writer.writerow([202, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])
        writer.writerow([203, 1, '12,23', 'this is a test title', 'this is a test title content', 1439514278, 1439514278])


if __name__ == '__main__':
    create_index()
    doc_add(docs)
    csv_file()
    csv_file2()
