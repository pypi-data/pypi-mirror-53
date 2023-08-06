"""Packaging settings."""

from os.path import abspath, dirname, join, isfile

from setuptools import setup

from cwlogcleaner import __version__

this_dir = abspath(dirname(__file__))
path = join(this_dir, 'README.rst')
long_description = ''
if isfile(path):
    with open(path) as file:
        long_description = file.read()

setup(
    name='cwlogcleaner',
    version=__version__,
    description='Utility to cleanup CloudWatch logs.',
    long_description=long_description,
    url='https://github.com/taimos/cwlogcleaner',
    author='Thorsten Hoeger',
    author_email='thorsten.hoeger@taimos.de',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='aws, cloud, cloudwatch, logs',
    packages=['cwlogcleaner'],
    install_requires=['boto3','inquirer'],
    entry_points={
        'console_scripts': [
            'cwlogcleaner=cwlogcleaner.cli:main',
        ],
    }
)
