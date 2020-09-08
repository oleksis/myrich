#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, Command


# Get the version from picta_dl/version.py without importing the package
exec(compile(open("myrich/version.py").read(), "myrich/version.py", "exec"))

DESCRIPTION = "Terminal emulator using Rich"
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="myrich",
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/oleksis/myrich",
    author="Oleksis Fraga",
    author_email="oleksis.fraga@gmail.com",
    license="MIT License",
    packages=[
        "myrich",
		"myrich.vendor",
    ],
    classifiers=[
        "Topic :: Terminal :: Rich",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Aproved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">3.6",
    entry_points={
        "console_scripts": ["myrich = myrich:main"]
    },
)