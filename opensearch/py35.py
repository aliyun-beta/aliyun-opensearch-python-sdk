import asyncio
from urllib.parse import urlencode
from . import const
try:
    import ujson as json
except ImportError:
    import json


async def aiohttp_client(session, url, params, method):
    """
        Use aiohttp http client library
    """
    if method == const.HTTP_GET:
        response = await session.get(url)
    elif method == const.HTTP_POST:
        headers = {}
        headers['content-type'] = 'application/x-www-form-urlencoded'
        response = await session.post(url, data=urlencode(params), headers=headers)
    else:
        raise

    if response.status == 200:
        try:
            body = await response.text()
            return json.loads(body)
        finally:
            await response.release()
