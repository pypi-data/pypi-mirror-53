#!/usr/bin/python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biggerquery",
    version="0.3.dev19",
    author=u"Chi",
    author_email="chibox-team@allegrogroup.com",
    description="BigQuery client wrapper with clean API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/allegro/biggerquery",
    packages=["biggerquery"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "google-cloud-bigquery>=1.12, <=1.18",
        "pandas>=0.23, <=0.24",
        "google-cloud-storage>=1.16, <=1.18",
        "mock>=3.0.5",
        "pyarrow>=0.14",
    ],
    extras_require={
        'beam': [
            'apache-beam==2.15.0',
            'avro>=1.8.2, <=1.9.0',
        ],
    },
)