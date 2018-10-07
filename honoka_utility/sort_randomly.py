# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import random
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i')

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    lines = []

    for line in open(args.input, 'r', 'utf-8'):
        lines.append(line.rstrip())

    random.shuffle(lines)

    for line in lines:
        print(line)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
