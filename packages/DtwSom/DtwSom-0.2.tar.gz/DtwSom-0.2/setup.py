#!/usr/bin/env python
from distutils.core import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(name='DtwSom',
      packages=['DtwSom'],
      version='0.2',
      description='Implementation of the Dynamic Time Warping Self Organizing Maps (DTW-SOM)',
      long_description=long_description,
      author='Kenan Li',
      author_email="kenanl@usc.edu",
      include_package_data=True,
      license="CC BY 3.0",
      install_requires=['numpy', 'fastdtw'],
      url='https://github.com/Kenan-Li/dtwsom',
      download_url='https://github.com/Kenan-Li/dtwsom/archive/master.zip',
      keywords=['self-organizing map', 'time series analysis', 'clustering', 'dimentionality reduction', 'dynamic time warping']
 )
