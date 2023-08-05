#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().splitlines()


setup(
    name="hou-flask",
    version="0.0.1",
    description="Basic authentication and authorization application",
    long_description=readme + "\n\n" + history,
    author="Tim Martin",
    author_email="oss@timmartin.me",
    url="https://github.com/timmartin19/hou-flask",
    packages=["houflask"],
    package_dir={"houflask": "houflask"},
    include_package_data=True,
    install_requires=requirements,
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
