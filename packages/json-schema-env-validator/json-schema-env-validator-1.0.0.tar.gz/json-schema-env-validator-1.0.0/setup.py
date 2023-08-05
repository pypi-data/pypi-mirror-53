# -*- coding: utf-8 -*-
from setuptools import setup

import os

_dir = os.path.dirname(os.path.realpath(__file__))

setup(
    name="json-schema-env-validator",
    version="1.0.0",
    description="",
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(_dir, "README.md")).read(),
    keywords=[],
    author="Nathan Van Gheem",
    author_email="vangheem@gmail.com",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/onna/enviral",
    packages=["enviral"],
    install_requires=["jsonschema"],
    extras_require={},
    entry_points={
        "console_scripts": ["json-schema-env-validator=enviral.command:main"]
    },
)
