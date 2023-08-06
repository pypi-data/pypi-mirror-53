#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [
    'apache-beam>=2.15.0',
    'google-cloud-storage>=1.20.0',
    'psycopg2>=2.8.3',
    'SQLAlchemy>=1.3.8',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    name='paralelocs_beam',
    version='0.3.5',
    description="Paraleo CS Custom packages to work with Apache Beam on Python SDK",
    author="Lucas Magalhaes",
    author_email='lucas.magalhaes@paralelocs.com.br',
    python_requires='>=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
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
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    keywords="apache beam paralelocs python sdk",
    packages=find_packages(include=['paralelocs_beam', 'paralelocs_beam.*'], exclude=['test', 'tests']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/paralelo/paralelocs_beam',
    zip_safe=False,
)
