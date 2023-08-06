============
asn1vnparser
============


.. image:: https://img.shields.io/pypi/v/asn1vnparser.svg
        :target: https://pypi.python.org/pypi/asn1vnparser

.. image:: https://img.shields.io/travis/mtannaan/asn1vnparser.svg
        :target: https://travis-ci.org/mtannaan/asn1vnparser

.. image:: https://readthedocs.org/projects/asn1vnparser/badge/?version=latest
        :target: https://asn1vnparser.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Parses ASN.1 value notation into a Python object or JSON without requiring its ASN.1 schema.


* Free software: MIT license
* Documentation: https://asn1vnparser.readthedocs.io.


Features
--------

* Parsing ASN.1 value notation into a Python object, or a JSON string
* No ASN.1 Schema Required

Limitations
-----------

* Since Knowledge of schema is not used, misdetection of ASN.1 types can occur; see Type Translations section.
* Some ASN.1 types and grammars are not supported; see grammar.py.

Type Translations
-----------------

`asn1vnparser` performs the following type translations:

======================================  =================  =============================  ==========================
ASN.1 Type                              Python Type        JSON Type                      Example (ASN.1 -> Python)
======================================  =================  =============================  ==========================
NULL                                    None               null                           NULL -> None
BOOLEAN                                 bool               True/False                     TRUE -> True
INTEGER                                 int                number (int)                   3 -> 3
REAL                                    float              number (real)                  0.1 -> 0.1
BIT STRING (^1)                         bitarray.bitarray  string (e.g. "010101")         '010101'B -> bitarray.bitarray('010101')
OCTET STRING (^1)                       bytes              string (e.g. "0123ab")         '0123AB'H -> b'\x01\x23\xab'
`cstring` (PrintableString, etc.)       str                string                         "foobar" -> 'foobar'
ENUMERATED                              str                string                         any-identifier -> 'any-identifier'
CHOICE                                  Dict[str, Any]     {"string": (any JSON object)}  alt1 : 123 -> {'alt1': 123}
Open Type  (e.g. type field)            Dict[str, Any]     {"String": (any JSON object)}  Type1 : 123 -> {'Type1': 123}
empty SEQUENCE or SEQUENCE OF           {} (empty dict)    {} (empty object)              {} -> {}, [] -> {}
SEQUENCE                                dict               object                         {f1 val, f2 1} -> {'f1': 'val', 'f2': 1}
SEQUENCE OF                             list               array                          [1, 2, 3] -> [1, 2, 3]
OBJECT IDENTIFIER                       List[int]          array of number (int)          {1 2 3} -> [1, 2, 3]
======================================  =================  =============================  ==========================

(^1) ``CONTAINING (some_value)`` is interpreted as simply ``(some_value)``, e.g.::

    {
        field1 123,
        field2 CONTAINING {
            field2-1 TRUE,
            field2-2 FALSE
        }
    }

is parsed into following Python object::

    {
        "field1": 123,
        "field2": {
            "field2-1": True,
            "field2-2": False
        }
    }




Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
