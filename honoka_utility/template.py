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
from lab import build_dirname, build_random_dirname

from honoka_utility import kernprof_preprocess
from honoka_utility import util

logger = logging.getLogger(__name__)


@click.command()
@click.argument('input')
@click.argument('output-top-dir')
@click.option('--lang', '-l',
              type=click.Choice(['ja', 'en']),
              default='ja')
@click.option('--params', '-p', default=[], multiple=True)
@click.option('--bool-opt', '-b', default=False, is_flag=True)
@click.option('--log-level',
              type=click.Choice(['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']),
              default='INFO')
def main(input,
         output_top_dir,
         lang,
         params,
         bool_opt,
         log_level):
    params = locals().copy()

    output_dir = os.path.join(output_top_dir, build_dirname(params))
    os.makedirs(output_dir, exist_ok=True)

    import logging
    import colorlog
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    stdout_handler = logging.StreamHandler()
    log_file = f'{output_dir}/log.txt'
    if os.path.exists(log_file):
        os.remove(log_file)
    file_handler = logging.FileHandler(log_file)
    for handler in [stdout_handler, file_handler]:
        handler.setFormatter(
            colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s [%(process)d] %(levelname)s %(name)s %(cyan)s%(message)s'))
        root_logger.addHandler(handler)

    print(f'logging to {log_file}')


if __name__ == '__main__':
    main()
