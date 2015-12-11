# coding=utf-8
import csv
import time
from . import const

try:
    import ujson as json
except ImportError:
    import json


const.PUSH_MAX_SIZE = 1.5 * 1024 * 1024     # 2MB
const.PUSH_FREQUENCY = 5    # 5 times/s


class IndexDoc(object):

    """
    This class provides adding documents, updating documents,
    delete documents, access to state of the specified document.
    >>> from opensearch import Client
    >>> from opensearch import IndexDoc
    >>> client = Client('app_key', 'app_secret', 'host')
    >>> indexDoc = IndexDoc(client, 'index_name')
    """

    def __init__(self, client, index_name):
        self.client = client
        self.index_name = index_name
        self.path = '/index/doc/' + index_name

    def get(self, docid, table_name):
        params = {
            'id': docid,
            'table_name': table_name,
        }
        return self.client.getResponse(self.path, params)

    def add(self, docs, table_name):
        """
        add one or more documents to table
        Args:
            docs (dict or list[dict]): one or more document
            table_name (str): opensearch table name
        """
        return self.action('add', docs, table_name)

    def update(self, docs, table_name):
        """
        update one or more documents to table
        Args:
            docs (dict or list[dict]): one or more document
            table_name (str): opensearch table name
        """
        return self.action('update', docs, table_name)

    def delete(self, doc_ids, table_name):
        """
        delete one or more documents
        Args:
            doc_ids (int or list[int]): one or more document id
            table_name (str): opensearch table name
        """
        if isinstance(doc_ids, list):
            docs = [{'id': _id} for _id in doc_ids]
        else:
            docs = [{'id': doc_ids}]
        return self.action('delete', docs, table_name)

    def action(self, cmd, docs, table_name):
        """
        Args:
            cmd (str): options: add, update, delete
            docs (dict or list[dict]): one or more document
            table_name (str): opensearch table name
        """
        if isinstance(docs, dict):
            docs = [{'cmd': cmd, 'fields': docs}]
        else:
            docs = [{'cmd': cmd, 'fields': d} for d in docs]

        params = {
            'action': 'push',
            'items': json.dumps(docs),
            'table_name': table_name,
            'sign_mode': 1,
        }
        return self.client.getResponse(self.path, params, method=const.HTTP_POST)

    def pushCSVFile(self, cmd, pathfile, table_name, offset, primary_key, multi_fields=None, max_size=const.PUSH_MAX_SIZE):
        """
        Batch csv document push
        Args:
            cmd (str): options: add, update, delete
            pathfile (str): csv file path
            table_name (str): opensearch table name
            offset (int): start push position
            primary_key (str): table primary key
            multi_fields (list[str]): multi-value fields
            max_size (int): push max size, opensearch limit 2MB, default: 1.5MB
        """
        docs = []
        fields = []
        field_size = 0
        push_size = 0
        line_num = 0
        log_file = pathfile + '.log'
        sleep_time = (1000/const.PUSH_FREQUENCY)/1000
        with open(log_file, 'a') as logfile:
            logfile.write('push start [%s] (%s)' % (pathfile, time.strftime('%Y-%m-%d %H:%M:%S')))
            logfile.write('\n')
            with open(pathfile, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    line_num += 1
                    if line_num == 1:
                        for field in row:
                            field_size += len(field) + 4
                            fields.append(field)
                        field_size += 2
                        if primary_key not in fields:
                            raise
                    else:
                        if offset and line_num <= offset:
                            continue
                        item = {}
                        for _id, val in enumerate(row):
                            push_size += field_size
                            push_size += len(val)
                            field_name = fields[_id]
                            if field_name in multi_fields:
                                val = val.split(',')
                                push_size += 2
                            item[field_name] = val
                        docs.append(item)
                        if push_size >= max_size:
                            if cmd == 'add':
                                self.add(docs, table_name)
                            elif cmd == 'update':
                                self.update(docs, table_name)
                            else:
                                raise
                            docs = []
                            push_size = 0
                            time.sleep(sleep_time)
                            logfile.write('pushed line: %s' % line_num)
                            logfile.write('\n')
            if docs:
                if cmd == 'add':
                    self.add(docs, table_name)
                elif cmd == 'update':
                    self.update(docs, table_name)
                else:
                    raise
                logfile.write('pushed line: %s' % line_num)
                logfile.write('\n')

            logfile.write('pushed complete [%s] (%s)' % (pathfile, time.strftime('%Y-%m-%d %H:%M:%S')))
            logfile.write('\n\n\n\n')
        return 'OK'
