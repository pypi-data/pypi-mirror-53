# -*- coding: utf-8 -*-

"""Defines `json.JSONEncoder` subclass
that makes parsed object (including bytes and bitarray) JSON-serializable
"""

import bitarray
import json
import sys


class JSONEncoder(json.JSONEncoder):
    """JSON encoder with additional support for bytes and bitarray

    Examples:

        >>> JSONEncoder().encode({"field1": 123})
        '{"field1": 123}'

        >>> JSONEncoder().encode({"field1": b'\x12\x34'})
        '{"field1": "1234"}'

        >>> JSONEncoder().encode({"field1": bitarray.bitarray('01010')})
        '{"field1": "01010"}'

        >>> JSONEncoder(compact_bitarray=True).encode({"field1": bitarray.bitarray('01010')})
        '{"field1": {"value": "50", "length": 5}}'

        >>> JSONEncoder().encode({"field1": {"Type": 567}})
        '{"field1": {"Type": 567}}'
    """

    def __init__(self, compact_bitarray=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._compact_bitarray = bool(compact_bitarray)

    def default(self, o):
        if isinstance(o, (bytes, bytearray)):
            return o.hex()
        elif isinstance(o, bitarray.bitarray):
            if self._compact_bitarray:
                return {'value': o.tobytes().hex(), 'length': len(o)}
            else:
                return o.to01()
        else:
            super().default(o)
