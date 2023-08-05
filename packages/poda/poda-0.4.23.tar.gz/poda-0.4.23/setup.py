from setuptools import setup, find_packages
from poda import *

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='poda',  # Required
    version=version,  # Required
    description='A package to wrap tensor operation',  # Required
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='gideonmanurung',  # Optional
    author_email='gideonmanurung3@gmail.com', #optional
    packages=["poda",
              "poda.application",
              "poda.object_detector",
              "poda.segmentation",
              "poda.transfer_learning", 
              "poda.preprocessing", 
              "poda.layers",
              "poda.utils"],  # Required
)