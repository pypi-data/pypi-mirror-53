# -*- coding: utf-8 -*-

"""Tokenizers and parsers."""

import re
from typing import Any, ClassVar, Dict, List, Type, Union

import bitarray
import pyparsing as pp

# --- X.680 --- #
# 12.2
typereference = pp.Word(initChars=pp.alphas.upper(),
                        bodyChars=pp.alphanums + '-')

# 12.3, 12.4
identifier = pp.Regex(r'[a-z]([a-zA-Z0-9\-]*[a-zA-Z0-9])?')
valuereference = identifier

# 12.8
number = pp.Regex(r'(0|[1-9][0-9]*)')

# 12.9
realnumber = pp.Regex(r'[0-9]+(\.([0-9]+)?)?([eE][\+\-]?(0|[1-9][0-9]+))?')


# --- global --- #

_forwarded_syntaxes = []


# --- classes --- #

class Meta_AddedToForwardedSyntaxes(type):
    """Adds classes into `_forwarded_syntaxes` on definition."""
    def __new__(cls, *args, **kwargs):
        new_class = super().__new__(cls, *args, **kwargs)
        _forwarded_syntaxes.append(new_class)
        return new_class


class AsnDefinition(object, metaclass=Meta_AddedToForwardedSyntaxes):
    """Base class for ASN.1 syntax."""

    # ## Syntax Definitions
    # Use `_raw_syntax` for non-recursive syntax definitions.
    # For recursive definitions,
    #     1. Defer syntax definition with `_raw_syntax = p.Forward()`
    #     2. Define a class method named `get_forwarded_syntax`
    #        with no argument which returns the syntax definition.
    #
    # ## Converting to Python object
    # Conversion can be done in __init__ method.
    # Receive tokens by `def __init__(self, toks: p.ParseResults)`
    # and set `self.value` to the Python object after conversion.

    _raw_syntax = None  # type: ClassVar[Type[pp.ParserElement]]

    @classmethod
    def syntax(cls) -> Type[pp.ParserElement]:
        cls._raw_syntax.setParseAction(cls)
        return cls._raw_syntax

    @classmethod
    def add_forwarded_syntax(cls):
        if hasattr(cls, 'get_forwarded_syntax'):
            cls._raw_syntax << (cls.get_forwarded_syntax())

    def __repr__(self):
        return super().__repr__()[:-1] + ' (value={})>'.format(repr(self.value))


# --- ASN.1 grammar components --- #

class AsnBoolean(AsnDefinition):
    """X.680 18.3"""
    def __init__(self, toks: pp.ParseResults):
        value = {
            'TRUE': True,
            'FALSE': False
        }[toks[0]]
        self.value = value  # type: bool

    _raw_syntax = pp.Keyword('TRUE') | pp.Keyword('FALSE')


class AsnInteger(AsnDefinition):
    """X.680 19.9"""
    def __init__(self, toks: pp.ParseResults):
        if 'SignedNumber' in toks:
            value = int(toks['SignedNumber'])
        elif 'identifier' in toks:
            value = toks['identifier']
        else:
            raise ValueError('unknown tokens for integer:', toks)

        self.value = value  # type: Union[int, str]

    _raw_syntax = (
        # (?!\.) is appended to avoid confision with realnumber
        pp.Regex(r'\-?(0|[1-9][0-9]*)(?!\.)').setResultsName('SignedNumber')
        | identifier.copy().setResultsName('identifier')
    )


class AsnEnumerated(AsnDefinition):
    """X.680 20.8"""
    def __init__(self, toks: pp.ParseResults):
        assert len(toks) == 1
        self.value = str(toks[0])

    _raw_syntax = identifier.copy()


class AsnReal(AsnDefinition):
    """X.680 21.6

    Limitations:
        - SequenceValue not supprted; parsed into dict by AsnSequence
    """
    def __init__(self, toks: pp.ParseResults):
        self.value = float(toks[0])

    _raw_syntax = (
        realnumber.copy()
        | (pp.Suppress(pp.Literal('-')) + realnumber.copy())
        | pp.Keyword('PLUS-INFINITY').setParseAction(lambda: 'inf')
        | pp.Keyword('MINUS-INFINITY').setParseAction(lambda: '-inf')
        | pp.Keyword('NOT-A-NUMBER').setParseAction(lambda: 'nan')
    )


class AsnBitString(AsnDefinition):
    """X.680 22.9

    limitations:
        - hstring not supported; parsed into bytes (not bitarray) 
            by AsnOctetstring
        - { identifierList } not supported; parsed into List[str] 
            by AsnSequenceOf and AsnEnumerated
        - {} not supported; parsed into {} (i.e. `dict()`) by AsnSequence
    """
    def __init__(self, toks: pp.ParseResults):
        if 'bstring' in toks:
            bits = re.sub(r'\s', '', toks['bstring'])
            value = bitarray.bitarray(bits)
        elif 'containing' in toks:
            value = toks['containing'].value
        else:
            raise ValueError('unknown toks for bit string: {}'.format(toks))

        self.value = value  # type: Union[bitarray.bitarray, Any]

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        return (
            pp.Suppress(pp.Literal('\''))
            + pp.Regex(r'[01\s]*').setResultsName('bstring')
            + pp.Suppress(pp.Literal('\'B'))
        ) | (
            pp.Suppress(pp.Keyword('CONTAINING'))
            + AsnValue.syntax().setResultsName('containing')
        )


class AsnOctetString(AsnDefinition):
    """X.680 23.3

    Limitations:

        - bstring not supported; parsed into bitarray (not bytes) by AsnBitstring
    """
    def __init__(self, s, loc, toks: pp.ParseResults):
        if 'hstring' in toks:
            hexstr = re.sub(r'\s', '', toks['hstring'])
            value = bytes.fromhex(hexstr)
        elif 'containing' in toks:
            value = toks['containing'].value
        else:
            raise ValueError('unknown toks for octet string: {}'.format(toks))

        self.value = value  # type: Union[bytes, Any]

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        return (
            pp.Suppress(pp.Literal('\''))
            + pp.Regex(r'([0-9A-Fa-f]{2}\s*)*').setResultsName('hstring')
            + pp.Suppress(pp.Literal('\'H'))
        ) | (
            pp.Suppress(pp.Keyword('CONTAINING'))
            + AsnValue.syntax().setResultsName('containing')
        )


class AsnNull(AsnDefinition):
    """X.680 24.3"""
    def __init__(self, toks: pp.ParseResults):
        self.value = None

    _raw_syntax = pp.Keyword('NULL')


class AsnSequence(AsnDefinition):
    """X.680 25.18"""
    def __init__(self, toks: pp.ParseResults):
        self.value = dict(
            (tok[0], tok[1].value) for tok in toks
        )  # type: Dict[str, Any]

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        lbrace = pp.Suppress(pp.Literal('{'))
        rbrace = pp.Suppress(pp.Literal('}'))
        comma = pp.Suppress(pp.Literal(','))
        empty = lbrace.copy() + rbrace.copy()

        content = pp.Group(identifier.copy() + AsnValue.syntax())
        contents = content + pp.ZeroOrMore(comma + content)
        non_empty = lbrace.copy() + contents + rbrace.copy()
        return empty | non_empty


class AsnSequenceOf(AsnDefinition):
    """X.680 26.3

    Limitations:

        - NamedValueList not supported; parsed into dict by AsnSequence
    """
    def __init__(self, toks: pp.ParseResults):
        self.value = [tok.value for tok in toks]  # type: List[Any]

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        lbrace = pp.Suppress(pp.Literal('{'))
        rbrace = pp.Suppress(pp.Literal('}'))
        comma = pp.Suppress(pp.Literal(','))
        empty = lbrace.copy() + rbrace.copy()

        content = AsnValue.syntax()
        contents = content + pp.ZeroOrMore(comma + content)
        non_empty = lbrace.copy() + contents + rbrace.copy()
        return empty | non_empty


class AsnChoice(AsnDefinition):
    """X.680 29.11"""
    def __init__(self, toks: pp.ParseResults):
        assert len(toks) == 2
        self.value = {toks[0]: toks[1].value}  # type: Dict[str, Any]

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        return (
            identifier.copy()
            + pp.Suppress(pp.Literal(':'))
            + AsnValue.syntax()
        )


class AsnObjectIdentifier(AsnDefinition):
    """X.680 32.3

    Limitations:

        - Only NumberForm supported
    """
    def __init__(self, toks: pp.ParseResults):
        self.value = [int(tok) for tok in toks]  # type: List[int]

    _raw_syntax = (
        pp.Suppress(pp.Literal(r'{}'))
        | (
            pp.Suppress(pp.Literal('{'))
            + pp.OneOrMore(number.copy())
            + pp.Suppress(pp.Literal('}'))
        )
    )


class AsnCString(AsnDefinition):
    """X.680 41.8 and 12.14

    Limitations:

        - character string forms other than `cstring` are not supported
        - following specification in 12.14 is not respected
            - The "cstring" may span more than one line of text, 
                in which case the character string being represented 
                shall not include spacing characters in the position 
                prior to or following the end of line in the "cstring".

    """
    def __init__(self, toks: pp.ParseResults):
        assert len(toks) == 1
        tok = toks[0]
        self.value = tok.replace("\"\"", "\"")  # type: str

    _raw_syntax = (
        pp.Suppress(pp.Literal("\""))
        + pp.Regex(r'([^\"]|\"\")*')
        + pp.Suppress(pp.Literal("\""))
    )


class AsnOpenTypeFieldVal(AsnDefinition):
    """X.681 14.6"""
    def __init__(self, toks: pp.ParseResults):
        assert len(toks) == 2
        self.value = {toks[0]: toks[1].value}  # type: Dict[str, Any]

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        return (
            typereference.copy()
            + pp.Suppress(pp.Literal(':'))
            + AsnValue.syntax()
        )


class AsnValue(AsnDefinition):
    """X.680 17.7

    Limitations:

        - Only supports value forms in get_forwarded_syntax
    """
    def __init__(self, s, loc, toks: pp.ParseResults):
        assert isinstance(toks, pp.ParseResults)
        self.value = toks[0].value  # type: Any

    _raw_syntax = pp.Forward()

    @classmethod
    def get_forwarded_syntax(cls):
        # note that this is composed by `|` operator,
        # i.e. `pyparsing.MatchFirst`
        return (
            # compound types
            AsnChoice.syntax()
            | AsnOpenTypeFieldVal.syntax()
            | AsnSequence.syntax()
            | AsnSequenceOf.syntax()
            | AsnObjectIdentifier.syntax()
            # not compound types
            | AsnNull.syntax()
            | AsnBoolean.syntax()
            | AsnInteger.syntax()
            | AsnReal.syntax()
            | AsnBitString.syntax()
            | AsnOctetString.syntax()
            | AsnCString.syntax()
            | AsnEnumerated.syntax()
        )


class AsnValueAssignment(AsnDefinition):
    """Object that represents ASN.1 value assignment (X.680 16.2).
    
    Parses::

        value_name TypeName ::= value

    Limitations:

        - Considers anything that matches `typereference` as `Type`
    
    Attributes:
        value_name (str): name of the assigned value.
        type_name (str): name of the value's type.
        value (Any): Python object that holds the value.
    """

    def __init__(self, toks: pp.ParseResults):
        assert len(toks) == 3
        self.value_name = str(toks[0])
        self.type_name = str(toks[1])
        self.value = toks[2].value  # type: Any

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__

    _raw_syntax = (
        valuereference.copy() + typereference.copy() +
        pp.Suppress('::=') + AsnValue.syntax()
    )


for _i in _forwarded_syntaxes:
    _i.add_forwarded_syntax()

# to be exported
value_syntax = pp.StringStart() + AsnValue.syntax()
value_assignment_syntax = pp.StringStart() + AsnValueAssignment.syntax()
