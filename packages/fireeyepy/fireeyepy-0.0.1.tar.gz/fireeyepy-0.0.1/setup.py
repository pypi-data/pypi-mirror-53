# Copyright (C) 2019 FireEye, Inc. All Rights Reserved.
from setuptools import setup

with open("README.md", "r") as f:
  long_description = f.read()
setup(
  name="fireeyepy",
  version="0.0.1",
  description="FireEye Client Library for Python",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/fireeye/fireeye-python",
  author="FireEye",
  author_email="developers@fireeye.com",
  license="MIT",
  packages=["fireeyepy"],
  platforms=["any"],
  install_requires=["requests>=2.4.2"],
  classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ]
)