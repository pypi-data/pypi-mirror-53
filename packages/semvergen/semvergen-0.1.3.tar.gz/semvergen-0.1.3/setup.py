# coding: utf-8

from setuptools import setup, find_packages
import imp
from os import path

_version = imp.load_source("semvergen._version", "semvergen/_version.py")

with open("README.md", "r") as fh:
    long_description = fh.read()

here = path.abspath(path.dirname(__file__))
requires = [l.strip() for l in open(path.join(here, "requirements.txt"), "r") if not l.startswith('#')]

setup(
    name='semvergen',
    version=_version.__version__,
    description="Semver Generator from Git tags",
    author_email="brad.janke@gmail.com",
    author="Brad Janke",
    url="https://github.com/bradj/semvergen",
    keywords=["semver", "generator"],
    install_requires=requires,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    long_description=long_description,
    scripts=['semvergen/bin/semvergen'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators"
    )
)
