# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from utility import util
import numpy
import logging

logger = logging.getLogger('utility.util_numpy')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def save_array(f_out, array):
    f_out.write(" ".join(map(str, array)) + "\n")


def load_array(f_in, dtype=numpy.float32):
    line = f_in.readline()
    words = line.rstrip().split()
    loaded_array = numpy.array([0.0] * len(words), dtype=dtype)
    for i, word in enumerate(words):
        loaded_array[i] = dtype(word)
    return loaded_array


def save_ndarray(f_out, ndarray):
    if len(ndarray.shape) == 1:
        f_out.write(" ".join(map(str, ndarray))+"\n")
    else:
        for row in ndarray:
            f_out.write(" ".join(map(str, row))+"\n")


def load_ndarray(f_in, num_row, num_col, dtype=numpy.float32, debug=False):
    loaded_ndarray = numpy.ndarray([num_row, num_col], dtype=dtype)
    for i_row, line in enumerate(f_in):
        words = util.split_string(line)
        for j_col, word in enumerate(words):
            logger.debug(str(num_row)+str(i_row)+str(j_col)+word)
            loaded_ndarray[i_row][j_col] = dtype(word)
        if i_row >= num_row:
            break
    return loaded_ndarray
