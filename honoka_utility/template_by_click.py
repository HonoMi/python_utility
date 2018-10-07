#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

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
from fn import _
from fn.monad import Option
from functional import seq
from collections import OrderedDict, defaultdict
from cytoolz import curry, partial, pipe, compose
from cytoolz.curried import *
from utility import util
from utility import kernprof_preprocess
import click
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--out', '-o', default=sys.stdout)
@click.option('--in_src', '-i', default=sys.stdin)
@click.option('--lang', '-l', type=click.Choice(['ja', 'en']), default='ja')
@click.option('--values', type=(int, int), default=(1, 2))
@click.option('--flag', is_flag=True)
@click.option('--upper', 'transformation', flag_value='upper')
@click.option('--lower', 'transformation', flag_value='lower', default=True)
@click.option('--shell', envvar='SHELL')
@click.argument('srces', nargs=-1)
def main(out, in_src, lang, values, flag, transformation, shell, srces):

    # How to use command.
    print(lang)
    print(values)
    print(flag)
    print(transformation)
    print(shell)

    # routines.
    f_out = util.get_f_out(out)
    f_in = util.get_f_in(in_src)

    for line in f_in:
        print(line.rstrip(), file=f_out)

    f_out.close()
    f_in.close()


if __name__ == "__main__":
    main()
