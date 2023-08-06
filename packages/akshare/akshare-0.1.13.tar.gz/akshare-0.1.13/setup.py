# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/9/30 13:58
contact: jindaxiang@163.com
desc: 从大连商品交易所、上海期货交易所、郑州商品交易所采集每日仓单数据, 建议下午 16:30 以后采集当天数据,
避免交易所数据更新不稳定导致的程序出错
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="akshare",
    version="0.1.13",
    author="Albert King",
    author_email="jindaxiang@163.com",
    description="a tools for downloading futures data from chinese commodity exchange!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jindaxiang/akshare",
    packages=setuptools.find_packages(),
    package_data={'': ['*.py', '*.json']},
    keywords=['futures', 'finance', 'spider'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
