# -*- coding: utf-8 -*-

"""Main module."""

from typing import Any, Union

from asn1vnparser import _grammar
from asn1vnparser import jsonencoder


def parse_asn1_value(asn1_value: str, as_json: bool = False) -> Union[Any, str]:
    r"""Converts ASN.1 value (mainly BuiltinValue in ITU-T Rec. X.680) to Python object.

    Args:
        asn1_value: a `str` representing ASN.1 value notation(s).

    Returns:

        - When `as_json` = False, a Python object representation of `asn1_value`
        - When `as_json` = True, a JSON representation of `asn1_value` as `str`

    Examples:

        >>> parse_asn1_value("123")  # INTEGER
        123

        >>> parse_asn1_value("{TRUE, FALSE}")  # SEQUENCE OF
        [True, False]

        >>> parse_asn1_value(
        ...     "{field1 NULL, field2 '1204'H, field3 '01011010 01'B}"
        ...     )  # SEQUENCE
        {'field1': None, 'field2': b'\x12\x04', 'field3': bitarray('0101101001')}

        >>> parse_asn1_value("alt1 : enum1")  # CHOICE
        {'alt1': 'enum1'}

        >>> parse_asn1_value("alt1: enum1", as_json=True)  # as_json
        '{"alt1": "enum1"}'
    """
    result = _grammar.value_syntax.parseString(asn1_value, parseAll=True)
    obj = result[0].value
    if as_json:
        return jsonencoder.JSONEncoder().encode(obj)
    else:
        return obj


def parse_asn1_value_assignment(
        asn1_val_assignment: str, as_json: bool = False) -> Union[_grammar.AsnValueAssignment, str]:
    """Converts ASN.1 value assignment to Python object.

    Args:
        asn1_value: a `str` representing ASN.1 value notation(s).

    Returns:

        - When `as_json` = False, a Python object representation of `asn1_value`
        - When `as_json` = True, a JSON representation of `asn1_value` as `str`

    Examples:

        >>> parse_asn1_value_assignment("valuename Typename ::= 1234")
        {'value_name': 'valuename', 'type_name': 'Typename', 'value': 1234}
    """
    result = _grammar.value_assignment_syntax.parseString(
        asn1_val_assignment, parseAll=True)
    obj = result[0]

    if as_json:
        return jsonencoder.JSONEncoder().encode(obj.__dict__)
    else:
        return obj
