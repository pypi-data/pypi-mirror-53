#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
from setup_utils import ROOT, DIRECTORY_NAME, read, read_section

README_NAME = "README.md"
PACKAGE_NAME = "fallback_view"

setup(
    name=DIRECTORY_NAME,
    version=read(("src", PACKAGE_NAME, "__init__.py",), "__version__"),
    description=read_section((README_NAME,), "Description", (0,)),
    long_description=read((README_NAME,)),
    long_description_content_type="text/markdown",
    author="Alex Seitsinger",
    author_email="contact@alexseitsinger.com",
    url="https://github.com/alexseitsinger/{}".format(DIRECTORY_NAME),
    install_requires=["Django"],
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests"]),
    include_package_data=True,
    license="BSD 2-Clause License",
    keywords=["django", "view", "middleware"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
)
