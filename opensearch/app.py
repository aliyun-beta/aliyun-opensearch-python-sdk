# coding=utf-8
from . import const


class IndexApp(object):

    def __init__(self, client):
        self.client = client
        self.__path = '/index'

    def create(self, index_name, template, method=const.HTTP_GET):
        """
        Args:
            index_name (str): index name
            template (str): template must have been created
            method (str): http method, options: const.HTTP_GET, const.HTTP_POST
        """
        path = self.__path + '/' + index_name
        return self.client.getResponse(path, {'action': 'create', 'template': template}, method)

    def delete(self, index_name, method=const.HTTP_GET):
        """
        Args:
            index_name (str): index name
            method (str): http method, options: const.HTTP_GET, const.HTTP_POST
        """
        path = self.__path + '/' + index_name
        return self.client.getResponse(path, {'action': 'delete'}, method)

    def status(self, index_name, method=const.HTTP_GET):
        """
        Args:
            index_name (str): index name
            method (str): http method, options: const.HTTP_GET, const.HTTP_POST
        """
        path = self.__path + '/' + index_name
        return self.client.getResponse(path, {'action': 'status'}, method)

    def getAll(self, page=None, size=None, method=const.HTTP_GET):
        """
        Args:
            page (int): page number
            size (int): page size
            method (str): http method, options: const.HTTP_GET, const.HTTP_POST
        """
        params = {}
        if page:
            params['page'] = page
        if size:
            params['page_size'] = size
        if not params:
            return self.client.getResponse(self.__path, method=method)
        else:
            return self.client.getResponse(self.__path, params, method)

    def rebuild(self, index_name, action, operate=None, table_name=None):
        """
        rebuild index
        Args:
            index_name (str): index name
            action (str): options: createtask
            operate (str): options: import
            table_name (str): table name
        """
        path = self.__path + '/' + index_name
        params = {}
        params['action'] = action
        if operate:
            params['operate'] = operate
        if table_name:
            params['table_name'] = table_name
        return self.client.getResponse(path, params)
