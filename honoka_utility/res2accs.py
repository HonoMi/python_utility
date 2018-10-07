# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re


class Index:

    def __init__(self):
        self.D = 0
        self.S = 0
        self.I = 0
        self.N = 0
        pass

    def reset(self):
        self.D = 0
        self.S = 0
        self.I = 0
        self.N = 0

    def get_H(self):
        return self.N - self.D - self.S

    def get_Err(self):
        return (1 - (self.get_H()) / self.N) * 100

    def get_Acc(self):
        return (1 - (self.get_H() - self.I) / self.N) * 100

    def print(self):
        print('CHAR: %ERR:' + str(self.get_Err()) +
              ', ACC ER=' + str(self.get_Acc()) +
              ' [H=' + str(self.get_H()) +
              ', D=' + str(self.D) +
              ', S=' + str(self.S) +
              ', I=' + str(self.I) +
              ', N=' + str(self.N) + ']')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_res', '-i')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    index = None
    for line in open(args.input_res, 'r'):
        if re.match('^".*', line):
            if index is not None:
                index.print()
            index = Index()
            print('\n' + line.rstrip())
            continue
        if re.match('^CHAR:.*', line):
            break
        words = line.rstrip().split()
        if len(words) == 2:
            index.N += 1
            continue
        err = words[2]
        if err == 'DEL':
            index.D += 1
            index.N += 1
        elif err == 'REP':
            index.S += 1
            index.N += 1
        elif err == 'INS':
            index.I += 1
    index.print()

if __name__ == "__main__":
    main()
