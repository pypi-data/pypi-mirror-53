=======
History
=======

0.2.0 (2019-10-02)
------------------
New Features
************

- Partial parsing of a value or a value assignment (``parse_all`` option)

.. code-block:: python

    >>> parse_asn1_value(
    ...     "alt1: enum1\n---this is remaining string---",
    ...     as_json=True,
    ...     parse_all=False)  # as_json
    ('{"alt1": "enum1"}', '\n---this is remaining string---')

- Parsing multiple value assignments

.. code-block:: python

    >>> parse_asn1_value_assignments(
    ...     'value1 INTEGER ::= 1\nvalue2 Type2 ::= the-value')
    [
        {'value_name': 'value1', 'type_name': 'INTEGER', 'value': 1},
        {'value_name': 'value2', 'type_name': 'Type2', 'value': 'the-value'}
    ]

Bug Fixes
*********

- CLI no longer crashes when given ``--json`` option.


0.1.0 (2019-09-29)
------------------

* First release on PyPI.
