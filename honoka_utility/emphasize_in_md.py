#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import sys
from utility import util
import pandas


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default=sys.stdin)
    parser.add_argument('--keywords', '-k', default='', help='Comma separated words.')
    parser.add_argument('--level', type=int, default=3)
    parser.add_argument('--emphasize_firstline', default=False, action='store_true')
    args = parser.parse_args()
    return args


def emphasize_firstline(text, level=3):
    tag = ''.join(['_'] * level)
    lines = text.split('\n')
    ret_text = tag + lines[0] + tag + '\n'
    ret_text += '\n'.join(lines[1:])
    return ret_text


def emphasize_keywords(text, keywords, level=3):
    tag = ''.join(['_'] * level)
    for keyword in keywords:
        text = re.sub(keyword, ' ' + tag + keyword + tag + ' ', text)
    return text


def main():
    args = get_args()

    keywords = re.split('[ 　\t,]+', args.keywords)
    keywords_sorted = sorted(keywords, key=lambda x:len(x))

    f_in = util.get_f_in(args.input)
    text = f_in.read()
    text = emphasize_keywords(text, keywords_sorted, level=args.level)
    if args.emphasize_firstline:
        text = emphasize_firstline(text, level=args.level)

    f_out = util.get_f_out(args.output)
    f_out.write(text)
    f_out.close()


if __name__ == "__main__":
    main()
