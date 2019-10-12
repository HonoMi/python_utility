import argparse
from argparse import RawTextHelpFormatter
import copy
import datetime
import io
import json
import logging
import math
import os
import pickle
import re
import sys
import tempfile
import time
from abc import ABC
from abc import abstractmethod
from collections import OrderedDict
from collections import defaultdict
from pdb import set_trace
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from cytoolz import compose
from cytoolz import curry
from cytoolz import partial
from cytoolz import pipe
from cytoolz.curried import *
from fn import _
from fn.monad import Option
from functional import seq

from honoka_utility import kernprof_preprocess
from honoka_utility import util

logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--input', '-i', default=sys.stdin)
    parser.add_argument('--lang', '-l', choices=['ja', 'en'])
    parser.add_argument('--params', nargs='+', default=[], help='--params hoge fuga piyo')
    parser.add_argument('--hoge-fuga', required=True)
    parser.add_argument('-b', action='store_true', default=False)

    parser.add_argument('--log_level',
                        choices=['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        default='WARNING')

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    # 以下はlogを使う側が行う．
    from log_handler import handler
    root_logger = logging.getLogger()
    root_logger.setLevel(args.log_level)
    root_logger.addHandler(handler)

    print(args.output_hoge)

    f_out = util.get_f_out(args.output)
    f_in = util.get_f_in(args.input)

    for line in f_in:
        print(line.rstrip(), file=f_out)

    f_out.close()
    f_in.close()


if __name__ == '__main__':
    main()
