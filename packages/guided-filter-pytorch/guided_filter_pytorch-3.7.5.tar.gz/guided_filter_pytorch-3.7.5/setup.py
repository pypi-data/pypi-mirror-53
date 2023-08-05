#!/usr/bin/env python
from setuptools import setup, find_packages

try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
   long_description = long_description.replace("\r", "")
except (IOError, ImportError):
    long_description = ''

setup(
    name="guided_filter_pytorch",
    version="3.7.5",
    description="Deep Guided Filtering Layer for PyTorch",
    long_description=long_description,
    url="https://github.com/wuhuikai/DeepGuidedFilter",
    author="wuhuikai",
    author_email="huikaiwu@icloud.com",
    # Exclude the build files.
    packages=find_packages(exclude=["test"]),
    zip_safe=True
)