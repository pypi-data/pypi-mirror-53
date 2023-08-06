# -*- coding: utf-8 -*-

"""Parses ASN.1 value notation into a Python object or JSON without requiring its ASN.1 schema."""

__version__ = '0.2.0'

from asn1vnparser._asn1vnparser import parse_asn1_value, parse_asn1_value_assignment, parse_asn1_value_assignments
from asn1vnparser._grammar import AsnValueAssignment

__all__ = ["AsnValueAssignment", "parse_asn1_value",
           "parse_asn1_value_assignment", "parse_asn1_value_assignments"]
