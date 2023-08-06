#!/usr/bin/env python
import os
from setuptools import setup

CWD = os.path.dirname(os.path.realpath(__file__))


def read(*path):
    filename = os.path.join(CWD, *path)
    with open(filename, "r") as f:
        return f.read()


setup(
    name="mnemonic",
    version="0.19",
    author="Trezor",
    author_email="info@trezor.io",
    description="Implementation of Bitcoin BIP-0039",
    long_description=read("README.rst"),
    url="https://github.com/trezor/python-mnemonic",
    packages=["mnemonic"],
    package_data={"mnemonic": ["wordlist/*.txt"]},
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
