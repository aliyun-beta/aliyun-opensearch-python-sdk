# coding=utf-8
from . import const

const.LOG_SORT_ASC = 'ASC'
const.LOG_SORT_DESC = 'DESC'


class ErrorLog(object):

    def __init__(self, client, index_name):
        self.client = client
        self.index_name = index_name
        self.path = '/index/error/' + index_name

    def call(self, page, size, sort_mode=const.LOG_SORT_ASC, method=const.HTTP_GET):
        """
        Get error log info
        Args:
            page (int): page number
            size (int): page size
            sort_mode (str): sort mode, options: const.LOG_SORT_ASC, const.LOG_SORT_DESC
            method (str): http method, options: const.HTTP_GET, const.HTTP_POST
        """
        params = {}
        params['page'] = page
        params['page_size'] = size
        params['sort_mode'] = sort_mode
        return self.client.getResponse(self.path, params, method)
