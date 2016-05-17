import os

from setuptools import setup, find_packages

VERSION = '0.0.3'

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='Django Dynamic Fixtures',
    version=VERSION,
    long_description=README,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    setup_requires=[
        'pytest-runner'
    ],
    install_requires=[
        'Django==1.7.*'
    ],
    tests_require=[
        'pytest',
        'pytest-django',
        'pytest-pythonpath',
        'mock==1.3.0',
    ],
    url='',
    license='MIT',
    author='Peter Slump',
    author_email='peter@yarf.nl',
    description='Install Dynamic Django fixtures.'
)
