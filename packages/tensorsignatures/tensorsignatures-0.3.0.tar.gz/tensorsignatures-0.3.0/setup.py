#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from pkg_resources import DistributionNotFound, get_distribution
from setuptools import setup, find_packages


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None

requirements = [
    'Click>=6.0',
    'scipy>=1.1.0',
    'pandas>=0.23.4',
    'h5py>=2.8.0',
    'numpy>=1.16.1',
    'scikit-learn>=0.20.0',
    'matplotlib>=3.0.2',
    'tensorflow>=1.10.1',
    'tqdm>=4.11.0']

if get_dist('tensorflow') is None and get_dist('tensorflow-gpu') is not None:
    requirements.remove('tensorflow>=1.10.1')


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Harald Sager Vohringer",
    author_email='harald.voeh@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6'
    ],
    description="Tensorframework for mutational signature analysis.",
    entry_points={
        'console_scripts': [
            'tensorsignatures=tensorsignatures.cli:main'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tensorsignatures',
    name='tensorsignatures',
    packages=find_packages(include=['tensorsignatures']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sagar87/tensorsignatures',
    version='0.3.0',
    zip_safe=False,
)
