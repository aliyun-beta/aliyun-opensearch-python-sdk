# coding=utf-8
import sys
import copy
import hashlib
import base64
import hmac
import uuid
import logging
from datetime import datetime
from operator import itemgetter

from . import const

try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    from urllib.parse import urlparse, urlencode, quote  # py 3.x
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode, quote  # py 2.x

try:
    import ujson as json
except ImportError:
    import json

client_requests = True
try:
    import requests
except ImportError:
    client_requests = False

client_aiohttp = False
PY_34 = sys.version_info >= (3, 4, 1)
PY_35 = sys.version_info >= (3, 5)
if PY_35:
    try:
        import aiohttp
        from .py35 import aiohttp_client
        client_aiohttp = True
    except ImportError:
        pass
elif PY_34:
    try:
        import aiohttp
        from .py34 import aiohttp_client
        client_aiohttp = True
    except ImportError:
        pass

const.HTTP_GET = 'GET'
const.HTTP_POST = 'POST'

logger = logging.getLogger(__name__)


class Client(object):

    """
    This class provides access to aliyun opensearch api http client.
    supports standard library httplib, requests and aiohttp. will be automatically adapted according to your environment.
    >>> from opensearch import Client
    >>> client = Client('app_key', 'app_secret', 'host')
    >>> client = Client('app_key', 'app_secret', 'host', lib="requests")
    """

    def __init__(self, key, secret, base_url, timeout=30, lib="auto", proxy=None, signatureMethod="HMAC-SHA1", SignatureVersion="1.0"):
        """
        Args:
            key (str): aliyun Access Key ID
            secret (str): aliyun Access Key Secret
            base_url (str): aliyun API url: http://opensearch-cn-hangzhou.aliyuncs.com
            timeout (int): request api timeout
            lib (str): default value is 'auto', options: auto, aiohttp, requests.
            proxy (str): http proxy url
            signatureMethod (str): default 'HMAC-SHA1'
            SignatureVersion (str): default '1.0'
        """

        version = 'v2'
        self.lib = lib
        self.sign_params = {
            'Version': version,
            'AccessKeyId': key,
            'SignatureMethod': signatureMethod,
            'SignatureVersion': SignatureVersion,
        }
        self.secret = secret
        self.base_url = base_url
        self.timeout = timeout
        self.proxy = proxy
        self.session = None
        if (self.lib == 'auto' or self.lib == 'requests') and client_requests:
            self.session = requests.session()
        if (self.lib == 'auto' or self.lib == 'aiohttp') and client_aiohttp:
            if self.proxy:
                conn = aiohttp.ProxyConnector(proxy=self.proxy)
            else:
                conn = aiohttp.TCPConnector()
            self.session = aiohttp.ClientSession(connector=conn)

    def getResponse(self, path, params=None, method=const.HTTP_GET):
        """
        Call aliyun opensearch api get response result.
        Args:
            path (str): api path
            params (dict): parameters request
            method (str): http method, default: 'GET': const.HTTP_GET, 'POST': const.HTTP_POST
        """
        if not params:
            params = {}
        params.update(self.sign_params)
        now = datetime.utcnow()
        params['Timestamp'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        params['SignatureNonce'] = str(uuid.uuid4())
        params['Signature'] = self.__sign(params, method)

        url = '%s%s' % (self.base_url, path)
        if method == const.HTTP_GET:
            url = '%s?%s' % (url, urlencode(params))

        if (self.lib == 'auto' or self.lib == 'aiohttp') and client_aiohttp:
            ret = aiohttp_client(self.session, url, params, method)
        elif (self.lib == 'auto' or self.lib == 'requests') and client_requests:
            ret = self.__requests(url, params, method, self.proxy)
        else:
            ret = self.__httplib(url, params, method, self.proxy)
        return ret

    def __httplib(self, url, params, method, proxy=None):
        """
        Use standard library httplib
        """
        parser = urlparse(url)
        scheme = parser.scheme
        if scheme == 'http':
            if proxy:
                proxy_parser = urlparse(proxy)
                if proxy_parser.port:
                    connection = httplib.HTTPConnection(proxy_parser.hostname, proxy_parser.port)
                else:
                    connection = httplib.HTTPConnection(proxy, 80)
            else:
                connection = httplib.HTTPConnection(parser.hostname, 80, self.timeout)
        else:
            raise const.ArgError('[%s] %s scheme not support' % (url, scheme))

        connection.connect()
        if method == const.HTTP_GET:
            connection.request(method, url)
        elif method == const.HTTP_POST:
            headers = {}
            headers['Content-type'] = 'application/x-www-form-urlencoded'
            connection.request(method, url, body=urlencode(params), headers=headers)
        else:
            raise const.ArgError('%s method not support' % method)

        response = connection.getresponse()
        if response.status == 200:
            body = response.read()
            return json.loads(body.decode("utf-8"))

    def __requests(self, url, params, method, proxy=None):
        """
        Use requests http client library
        """
        proxies = {}
        if proxy:
            proxies = {"http": proxy}
        if method == const.HTTP_GET:
            response = self.session.get(url, proxies=proxies)
        elif method == const.HTTP_POST:
            headers = {}
            headers['Content-type'] = 'application/x-www-form-urlencoded'
            response = self.session.post(url, params, headers=headers, proxies=proxies)
        else:
            raise const.ArgError('%s method not support' % method)

        if response.status_code == 200:
            return json.loads(response.text)

    def __sign(self, params={}, method=const.HTTP_GET):
        if 'sign_mode' in params and params['sign_mode'] == 1:
            params = copy.copy(params)
            del params['items']

        query = '&'.join(self.__percent_encode(k) + '=' + self.__percent_encode(v)
                         for k, v in sorted(params.items(), key=itemgetter(0)))

        base_string = method.upper() + '&%2F&' + self.__percent_encode(query)
        b64string = base64.b64encode(hmac.new((self.secret + '&').encode(), base_string.encode(), hashlib.sha1).digest())
        return b64string

    def __percent_encode(self, string):
        return quote(str(string)).replace('+', '%20').replace('*', '%2A').replace('%7E', '~').replace('/', '%2F')
