#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='opensearch',
    version='0.1.0',
    description='Aliyun OpenSearch SDK',
    author='Hongbo Jin',
    author_email='jin_hb_zh@126.com',
    py_modules=['opensearch', ],
    packages=['opensearch'],
    url='',
    license="",
    long_description=open('README.md').read(),
    install_requires=[
    ],
    classifiers=[
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ])
