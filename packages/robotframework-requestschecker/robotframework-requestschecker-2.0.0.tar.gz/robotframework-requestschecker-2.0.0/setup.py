"""Setup module for Robot Framework Requests Checker Library package."""

# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get install requires from requirements.txt
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='robotframework-requestschecker',
    version='2.0.0',
    description='Robot Framework Library For Checking HTTP Response Status Codes',
    long_description=long_description,
    url='https://github.com/peterservice-rnd/robotframework-requestschecker',
    author='JSC PETER-SERVICE',
    author_email='mf_aist_all@billing.ru',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Robot Framework :: Library',
    ],
    keywords='testing testautomation robotframework logging autotest requests http response code',
    package_dir={'': 'src'},
    py_modules=['RequestsChecker'],
    install_requires=requirements,
)
