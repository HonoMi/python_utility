# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys
import re
from utility import util, kernprof_preprocess
from nlp import idseq


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default='__stdin__')
    parser.add_argument('--func_name', default='ydseq2jp')
    parser.add_argument('--line_by_line', action='store_true', default=False)
    parser.add_argument('--map_unk_str', default='FFFFFFFF')
    parser.add_argument('--split_and_splice', action='store_true', default=False)
    parser.add_argument('--remove_ng_words', action='store_true', default=False)
    parser.add_argument('--Lutz', action='store_true', default=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    lexicon_module = None
    if args.Lutz:
        from lexicon_module import lexicon_module
    else:
        from nlp import idseq as lexicon_module

    f_out = sys.stdout
    if args.output is not sys.stdout:
        util.mkdir(util.dirname(args.output))
        f_out = open(args.output, 'w')
    decode = getattr(lexicon_module, args.func_name)
    options = {}
    if args.func_name.find('jp2') >= 0:
        options = {'split_and_splice': args.split_and_splice}
    if not re.match('.*maseq.*', args.func_name) and not re.match('.*2jp', args.func_name):
        options['remove_ng_words'] = args.remove_ng_words
    options['map_unk_str'] = args.map_unk_str
    with util.open_(args.input) as f_in:
        if args.line_by_line:
            for line in f_in:
                print(decode(line.rstrip(), **options), file=f_out)
                sys.stdout.flush()
        else:
            print(decode(f_in.read(), **options), file=f_out)
    f_out.close()


if __name__ == "__main__":
    main()
