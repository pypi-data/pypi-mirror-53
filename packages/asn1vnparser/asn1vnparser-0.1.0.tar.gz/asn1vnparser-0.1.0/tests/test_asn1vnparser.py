#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `asn1vnparser` package."""


import json
import pathlib
import unittest

import asn1vnparser


class TestAsn1vnparser(unittest.TestCase):
    """Tests for `asn1vnparser` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_json(self):
        """
        Test conversion to JSON representations.
        """

        cases_dir = pathlib.Path(__file__).parent / 'cases'

        asn_strs = {
            asn_path.stem: asn_path.read_text()
            for asn_path in cases_dir.glob('*.asn')
        }
        json_strs = {
            json_path.stem: json_path.read_text()
            for json_path in cases_dir.glob('*.json')
        }

        assert set(asn_strs.keys()) == set(json_strs.keys())
        assert len(asn_strs) > 0

        for key in asn_strs:
            with self.subTest(key=key):
                res_json = asn1vnparser.parse_asn1_value_assignment(
                    asn_strs[key], as_json=True)
                res_py = json.loads(res_json)
                self.maxDiff = None
                self.assertEqual(res_py, json.loads(json_strs[key]))

    def test_command_line_interface(self):
        """Test the CLI."""
        # TODO: CLI testing
        pass

        #assert result.exit_code == 0
        #assert 'asn1vnparser.cli.main' in result.output

        #help_result = runner.invoke(cli.main, ['--help'])
        #assert help_result.exit_code == 0
        #assert '--help  Show this message and exit.' in help_result.output
