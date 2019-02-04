#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import copy
import datetime
import io
import math
import os
import pickle
import re
import sys
import time
import tempfile
import json
from pdb import set_trace
from fn import _
from fn.monad import Option
from functional import seq
from collections import OrderedDict, defaultdict
from cytoolz import curry, partial, pipe, compose
from cytoolz.curried import *
from honoka_utility import util
from honoka_utility import kernprof_preprocess
import logging
import coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default=sys.stdin)
    parser.add_argument('--lang', '-l', choices=['ja', 'en'])
    parser.add_argument('--params', nargs='+', default=[], help='--params hoge fuga piyo')
    parser.add_argument('-b', action='store_true', default=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    f_out = util.get_f_out(args.output)
    f_in = util.get_f_in(args.input)

    for line in f_in:
        print(line.rstrip(), file=f_out)

    f_out.close()
    f_in.close()


if __name__ == '__main__':
    main()
