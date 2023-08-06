"""
==============
Hi Hy Lang
==============
A simple package in Hy language that says Hi.

Its main purpose is to show how to create and publish a Python package that
contains Hy code.

See GitHub repository for the Hy package publication guide.
"""
from setuptools import setup,find_packages

setup(
	name='hihydebugaa',
	version='0.1.1',
	author='Alex Anggada',
	license='gpl-3.0',
	packages=find_packages(exclude=['tests*']),
	package_data={
		'hihydebugaa': ['*.hy']
	},
	include_package_data=True,
	zip_safe=False,
	platforms='any',
	install_requires=[
		'hy'
	]
)
