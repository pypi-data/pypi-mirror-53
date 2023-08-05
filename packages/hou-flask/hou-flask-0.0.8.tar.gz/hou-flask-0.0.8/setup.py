#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()


setup(
    name="hou-flask",
    version="0.0.8",
    description="Basic authentication and authorization application",
    long_description=readme + "\n\n" + history,
    author="Tim Martin",
    author_email="oss@timmartin.me",
    url="https://github.com/timmartin19/hou-flask",
    packages=find_packages(),
    package_data={"hou-flask": ["README.md", "HISTORY.md"]},
    include_package_data=True,
    install_requires=[
        "hou-flask-psycopg2",
        "python-rapidjson",
        "flask",
        "connexion",
        "werkzeug",
        "ultra-config",
        "jsonschema<3.0.0",
        "beaker",
        "boto3",
        "python-jose",
        "flask-wtf",
        "pystatuschecker",
        "factory-boy",
    ],
    zip_safe=False,
    keywords="houflask",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests",
)
