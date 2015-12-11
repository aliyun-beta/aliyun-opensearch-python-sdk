# coding=utf-8
from . import const


class Suggest(object):

    def __init__(self, client, index_name):
        self.client = client
        self.index_name = index_name
        self.path = '/suggest'

    def call(self, query, suggest_name, hit=10):
        """
        Args:
            query (str): query string
            suggest_name (str): suggest rule name
            hit (int): hit number, value range 1-10, default: 10
        """
        params = {}
        params["query"] = query
        params["index_name"] = self.index_name
        params["suggest_name"] = suggest_name
        params['hit'] = hit
        return self.client.getResponse(self.path, params, method=const.HTTP_GET)
