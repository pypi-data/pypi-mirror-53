# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-09-29.
# Copyright (c) 2019 3KWan.
# Description :
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fast-stl",
    version="1.0.0",
    description="fast project standard template library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="#Suyghur",
    author_email="Suyghurmjp@outlook.com",
    license="MIT License",
    packages=find_packages(),
    platforms=["all"],
    url="https://github.com/Suyghur/fast-stl",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries"
    ],
)
