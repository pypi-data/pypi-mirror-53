#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", 'r',encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "fileoperate",
    version = "1.0.1",
    author = "Jarno Yuan",
    author_email = "ykq12313@gmail.com",
    description = "A module to operate many kinds of files.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/yuanke7/fileoperate_package",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)