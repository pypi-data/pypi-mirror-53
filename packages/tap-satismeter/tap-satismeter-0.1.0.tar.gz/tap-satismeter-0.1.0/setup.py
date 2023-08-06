#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-satismeter",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_satismeter"],
    install_requires=[
        "singer-python>=5.0.12",
        "requests>=2.22.0",
        "arrow>=0.14.5",
        "tenacity>=5.0.4",
    ],
    entry_points="""
    [console_scripts]
    tap-satismeter=tap_satismeter:main
    """,
    packages=["tap_satismeter"],
    package_data = {
        "schemas": ["tap_satismeter/schemas/*.json"]
    },
    include_package_data=True,
)
