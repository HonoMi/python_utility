#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys
import json
from utility import util


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default=sys.stdin)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    f_out = util.get_f_out(args.output)
    f_in = util.get_f_in(args.input)

    json_obj = json.load(f_in)
    json.dump(json_obj, f_out, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    f_out.close()
    f_in.close()


if __name__ == "__main__":
    main()
