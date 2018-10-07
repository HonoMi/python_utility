# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import math
import re
import sys
from utility import util


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i')
    args = parser.parse_args()
    return args


def is_no_content(line):
    if re.match('^[ \t]*$', line):
        return True
    if re.match('^.*end.*$', line):
        return True
    if re.match('^.*==.*$', line):
        return True

    return False


def main():
    args = get_args()

    f_out = sys.stdout
    if args.output != sys.stdout:
        util.mkdir(util.dirname(args.output))
        f_out = open(args.output, 'w')

    gram_n = 0
    sum_prob = 0
    for line in open(args.input, 'r'):
        if is_no_content(line):
            continue
        if re.match('^..-grams:$', line):
            gram_n = int(re.sub('.*(.)-grams:', '\g<1>', line))
            continue
        if gram_n >= 2:
            break
        if gram_n == 1:
            fields = line.rstrip().split()
            sum_prob += math.pow(10, float(fields[0]))
    print(sum_prob)

    f_out.close()


if __name__ == "__main__":
    main()
