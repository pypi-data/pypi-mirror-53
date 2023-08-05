# -*- coding: utf-8 -*-
from yodine.version import VERSION_STR
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()

except IOError:
    long_description = ""


setup(
    name="Yodine",
    version=VERSION_STR,
    description="A simple pyglet-powered 2D game engine, with simple multiplayer support.",
    license="MIT",
    author="Gustavo6046",
    packages=find_packages(),
    install_requires=[r for r in open('requirements.txt').read().split('\n') if r],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ],
)
