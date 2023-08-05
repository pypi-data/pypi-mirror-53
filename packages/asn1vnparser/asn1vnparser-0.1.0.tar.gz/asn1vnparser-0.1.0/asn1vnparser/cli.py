# -*- coding: utf-8 -*-

"""Console script for asn1vnparser."""
import argparse
import json
import pathlib
import sys

import asn1vnparser


def main():
    """Console script for asn1vnparser.
    
    See `python cli.py --help`."""
    parser = argparse.ArgumentParser(
        prog='asn1vnparser',
        description='Prints out Python object (repr) or JSON for an ASN.1 value.')
    parser.add_argument('input_file', nargs='?', default='-',
                        help='input file path. Pass - (a single hypehn) to read from stdin.')
    parser.add_argument('-e', '--encoding', default=None,
                        help='input file encoding')
    parser.add_argument('-v', '--value_only', action='store_true',
                        help='parses an ASN.1 value (e.g. "3"), not a value assignment (e.g. "value Type ::= 3")')
    parser.add_argument('-j', '--json', action='store_true',
                        help='prints out JSON obejct. By default, this program prints out repr() of the resulting python object.')
    parser.add_argument('-o', '--output_file', nargs='?', default=None,
                        help='output file path. By default this program print the result to stdout.')
    parser.add_argument('-f', '--force', action='store_true',
                        help='force to overwrite an existing file.')
    args = parser.parse_args()

    if args.input_file == '-':
        input_str = sys.stdin.read()
    else:
        input_str = pathlib.Path(args.input_file).read_text(
            encoding=args.encoding)

    if args.value_only:
        ret_value = asn1vnparser.parse_asn1_value(input_str, as_json=args.json)
    else:
        ret_value = asn1vnparser.parse_asn1_value_assignment(
            input_str, as_json=args.json)
        ret_value = ret_value.__dict__

    if args.json:
        ret_str = ret_value
    else:
        ret_str = repr(ret_value)

    if args.output_file:
        output_path = pathlib.Path(args.output_file)
        if args.force or not output_path.exists():
            output_path.write_text(ret_str)
        else:
            raise FileExistsError(
                'output file already exists: {}'.format(args.output_file))
    else:
        print(ret_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
