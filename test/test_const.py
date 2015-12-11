# coding=utf-8

import pytest
from opensearch import const


def test_const_def():
    with pytest.raises(const.ConstError):
        const.HTTP_GET = 'get'


def test_const_del():
    with pytest.raises(const.ConstError):
        del const.HTTP_GET


def test_const_del2():
    with pytest.raises(AttributeError):
        del const.HTTP_GET2
