# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

import mojimoji
from utility import util


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default='__stdin__')
    parser.add_argument('--type', default='han_to_zen', help='[zen_to_han|han_to_zen]')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    encode = getattr(mojimoji, args.type)
    f_out = args.output
    if args.output is not sys.stdout:
        util.mkdir(util.dirname(args.output))
        f_out = open(args.output, 'w')

    with util.open_(args.input) as in_mod:
        for line in in_mod:
            print(encode(line.rstrip()), file=f_out)


if __name__ == "__main__":
    main()
