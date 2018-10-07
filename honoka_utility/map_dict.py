# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import sys
from utility import util


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', default='__stdin__')
    parser.add_argument('--dic', '-d',
                        default='/nraid/data61/morisita/KML_clone/nraid/data57/morisita/data/corpus/CLX/dic/ygcid2jp.txt',
                        help='default : $CLX/dic/ygcid2jp.txt')
    parser.add_argument('--additional_dic', '-ad', default=None)
    parser.add_argument('--distinguish_upper_lower', '-ul',
                        default='True', help='default : True')
    parser.add_argument('--map_unk_word_to', '-unk',
                        default="as_it_is", help='default : as_it_is')
    parser.add_argument('--target_column', '-c', default=-1,
                        type=int, help='default : all(-1)')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    dic = {}
    for line in open(args.dic):
        key, value = line.rstrip().split()
        dic[key] = value
        if args.distinguish_upper_lower == 'False':
            dic[key.upper()] = value
            dic[key.lower()] = value

    adic = {}
    if args.additional_dic is not None:
        for line in open(args.additional_dic):
            key, value = line.rstrip().split()
            adic[key] = value
            if args.distinguish_upper_lower == 'False':
                dic[key.upper()] = value
                dic[key.lower()] = value

    for line in util.open(args.input):
        words = line.rstrip().split()
        converted = util.map_dic(
            words, dic, target_column=args.target_column)
        converted = util.map_dic(
            converted, adic, target_column=args.target_column)
        print(' '.join(converted))
        sys.stdout.flush()

    return


if __name__ == "__main__":
    main()
