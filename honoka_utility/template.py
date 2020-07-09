#!/usr/bin/env python
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

import click
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


@click.command()
@click.argument('output')
@click.option('--input', '-i', default=sys.stdin)
@click.option('--lang', '-l',
              type=click.Choice(['ja', 'en']),
              default='ja')
@click.option('--params', '-p', default=[], multiple=True)
@click.option('--bool-opt', '-b', default=False, is_flag=True)
@click.option('--log-level',
              type=click.Choice(['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']),
              default='INFO')
def main(output,
         input,
         lang,
         params,
         bool_opt,
         log_level):

    import logging
    import colorlog
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s [%(process)d] %(levelname)s %(name)s %(cyan)s%(message)s'))
    root_logger.addHandler(handler)

    f_out = util.get_f_out(output)
    f_in = util.get_f_in(input)

    for line in f_in:
        print(line.rstrip(), file=f_out)

    f_out.close()
    f_in.close()


if __name__ == '__main__':
    main()
