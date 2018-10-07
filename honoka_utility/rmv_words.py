# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--ng_word_list', '-ng')
    parser.add_argument('--input', '-i')

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    ng_word_dict = {}
    for line in open(args.ng_word_list, 'r'):
        ng_word_dict[line.rstrip()] = 1

    for line in open(args.input, 'r'):
        words = line.rstrip().split()
        words_without_ng = []
        for word in words:
            if word not in ng_word_dict:
                words_without_ng.append(word)
        if len(words_without_ng) == 0:
            continue

        print(" ".join(words_without_ng))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
