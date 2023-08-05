#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['bitarray>=0.8.3', 'pyparsing>=2.4.2']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="mtannaan",
    author_email='12782884+mtannaan@users.noreply.github.com',
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Parses ASN.1 value notation into a Python object or JSON without requiring its ASN.1 schema.",
    entry_points={
        'console_scripts': [
            'asn1vnparser=asn1vnparser.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='asn1vnparser',
    name='asn1vnparser',
    packages=find_packages(include=['asn1vnparser', 'asn1vnparser.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mtannaan/asn1vnparser',
    version='0.1.0',
    zip_safe=False,
)
