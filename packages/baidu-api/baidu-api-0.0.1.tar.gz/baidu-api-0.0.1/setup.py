#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-26 10:16:11

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baidu-api",
    version="0.0.1",
    author="Xiang Wang",
    author_email="ramwin@qq.com",
    description="the python sdk for baidu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramwin/baidu-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        "redis",
        "requests",
    ],
)
