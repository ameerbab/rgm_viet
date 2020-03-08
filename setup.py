# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in rgm_vn/__init__.py
from rgm_vn import __version__ as version

setup(
	name='rgm_vn',
	version=version,
	description='RGM VN',
	author='emails@iwex.in',
	author_email='emails@iwex.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
