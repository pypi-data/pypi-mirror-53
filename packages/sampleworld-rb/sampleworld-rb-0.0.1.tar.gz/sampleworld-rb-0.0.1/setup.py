#!/usr/bin/env python
import setuptools
from distutils.core import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(name='sampleworld-rb',
      version='0.0.1',
      description='Just a sample package for python package development',
      author='Rizwan Hameed',
      author_email='rizwanbutt314@gmail.com',
      url='https://github.com/rizwanbutt314/python-package-development',
      py_modules=['sampleworld'],
      setup_requires=['pytest'],
      package_dir={'': 'src'},
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
