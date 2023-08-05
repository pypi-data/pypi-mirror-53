#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integrates doctests into unittest (and `setup.py test`)."""


import doctest
import unittest

from asn1vnparser import _asn1vnparser, _grammar, jsonencoder


def load_tests(_loader, tests, _ignore):
    tests.addTests(doctest.DocTestSuite(_asn1vnparser))
    tests.addTests(doctest.DocTestSuite(_grammar))
    tests.addTests(doctest.DocTestSuite(jsonencoder))
    return tests
