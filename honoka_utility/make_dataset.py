# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import argparse
import re
import random
import subprocess
from utility import util


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_top_dir', '-o')
    parser.add_argument('--seed_corpus', '-seed', help='The original corpus.')
    parser.add_argument('--sentences', '-sent',
                        help='\'num_train, num_valid, num_eval\'')
    parser.add_argument('--random_sort', default=False, action='store_true')
    parser.add_argument('--iteration', '-iter', default=1, type=int)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    util.mkdir(args.output_top_dir)
    subprocess.call('rm ' + args.output_top_dir + '/* 1>/dev/null 2>/dev/null', shell=True)

    lines = open(args.seed_corpus, 'r').readlines()
    if args.random_sort:
        random.shuffle(lines)

    num_train, num_valid, num_eval = list(map(int, re.split(', ', args.sentences)))
    if len(lines) < num_train + num_valid + num_eval:
        return

    # first make eval set once.
    eval_lines = lines[0:num_eval]
    if len(eval_lines) == num_eval:
        eval_file = args.output_top_dir + '/eval-' + util.zerofill(str(num_eval), num_fill=12)
        open(eval_file, 'w').write(''.join(eval_lines))

    # second, shuffle lines and extract train/valid lines for iteration times.
    train_valid_lines = lines[num_eval:]
    for iter in range(0, args.iteration):
        output_dir = args.output_top_dir + '/iter-' + str(iter)
        subprocess.call('rm ' + output_dir + '/* 1>/dev/null 2>/dev/null', shell=True)
        util.mkdir(output_dir)

        train_lines = train_valid_lines[0:num_train]
        valid_lines = train_valid_lines[num_train:num_train + num_valid]

        if len(train_lines) == num_train:
            filename = output_dir + '/train-' + util.zerofill(str(num_train), num_fill=12)
            open(filename, 'w').write(''.join(train_lines))
        if len(valid_lines) == num_valid:
            filename = output_dir + '/valid-' + util.zerofill(str(num_valid), num_fill=12)
            open(filename, 'w').write(''.join(valid_lines))
        if len(eval_lines) == num_eval:
            filename = output_dir + '/eval-' + util.zerofill(str(num_eval), num_fill=12)
            subprocess.call('ln -s `readlink -f ' + eval_file + '` ' + filename, shell=True)

        random.shuffle(train_valid_lines)

if __name__ == '__main__':
    main()
