#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['SQLAlchemy','apache_beam[gcp]', 'google-cloud-storage', 'psycopg2']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Lucas Magalhaes",
    author_email='lucas.magalhaes@paralelocs.com.br',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Paraleo CS Custom packages to work with Apache Beam on Python SDK",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    keywords=['beam','apache','paralelocs', 'python sdk','apache beam'],
    name='paralelocs_beam',
    packages=find_packages(include=['paralelocs_beam', 'paralelocs_beam.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/paralelo/paralelocs_beam',
    version='0.3.0',
    zip_safe=False,
)
