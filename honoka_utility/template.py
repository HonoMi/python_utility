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
import glob
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
from pathlib import Path

import click
from joblib import Parallel, delayed
from cytoolz import compose
from cytoolz import curry
from cytoolz import partial
from cytoolz import pipe
from cytoolz.curried import *
from fn import _
from fn.monad import Option
from functional import seq

from lab import build_dir, build_random_dir
from qsub_launcher import get_launcher
from logger_setup import setup as setup_logger

logger = logging.getLogger(__name__)


def extract_nbest(output_top_dir,
                  candidate_tsv,
                  nbest):
    params = json.load(open(candidate_tsv.parent / 'params.json'))

    output_params = params.copy()
    output_params['nbest_for_ranking'] = nbest
    output_dir = build_dir(output_params,
                           top_dir=output_top_dir,
                           name_exclude_keys=['model_1st_path',
                                              'model_1st_bpecode_path',
                                              'dataset_tsv',
                                              'implementation'],
                           save_params=True)

    df = pd.read_csv(candidate_tsv, sep='\t', index_col=0)

    def extract_nbest(row):
        best_n_indexes = []
        for idx, candidate_name in enumerate(row['candidate_names']):
            if int(re.sub(r'.*best_n--([0-9]*)$', r'\g<1>', candidate_name)) < nbest:
                best_n_indexes.append(idx)
        for col_name in df.columns:
            if col_name in ['reference']:
                continue
            vals = row[col_name]
            row[col_name] = [vals[idx] for idx in best_n_indexes]
        return None

    df.apply(extract_nbest, axis=1)

    output_path = output_dir / 'candidates.tsv'
    df.to_csv(output_path, sep='\t')
    logger.info('Write to "%s"', output_path)


@click.command()
@click.option('--input-top-dir', default='./output/140.create_ranking_features/')
@click.option('--output-top-dir', default='./output/141.extract_nbest/')
@click.option('--max-nbest', default=5, type=int)
@click.option('--num-workers', type=int, default=20)
@click.option('--log-level',
              type=click.Choice(['CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']),
              default='INFO')
def main(input_top_dir,
         output_top_dir,
         max_nbest,
         num_workers,
         log_level='INFO',
         **kwargs):
    output_top_dir = Path(output_top_dir)
    output_top_dir.mkdir(exist_ok=True, parents=True)

    setup_logger(filepaths=[output_top_dir / 'log.txt'], level=log_level)

    candidate_tsvs = sorted(Path(input_top_dir).glob('**/candidates.tsv'))
    jobs = []
    for candidate_tsv in candidate_tsvs:
        for nbest in range(1, max_nbest + 1):
            jobs.append(
                delayed(extract_nbest)(
                    output_top_dir,
                    candidate_tsv,
                    nbest)
            )

    Parallel(n_jobs=num_workers, backend='multiprocessing')(jobs)

if __name__ == '__main__':
    main()
