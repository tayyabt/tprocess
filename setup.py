import sys
import os
import codecs

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup


packages = [
	'tprocess',
]


if sys.argv[-1] == 'publish':
	os.system('python3 setup.py sdist upload')  # bdist_wininst
	sys.exit()




with codecs.open('README.md', 'r', 'utf-8') as f:
	readme = f.read()


setup(
	name='tprocess',
	version='0.1',
	description='A simple package for communicating with subprocesses (like pexpect) without the dreaded 1024 input limit.',
	long_description=readme,
	author='Tayyab Tariq',
	author_email='tayyabt@gmail.com',
	url='https://github.com/tayyabt/tprocess',
	packages=packages,
	include_package_data=True,
	license='MIT',
	zip_safe=False,
	classifiers=[
		'Programming Language :: Python :: 3',
		'Natural Language :: English',
		'Intended Audience :: Developers',
	],
)
