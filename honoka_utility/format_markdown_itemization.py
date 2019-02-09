#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import sys
from fn import _
from functional import seq


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default=sys.stdin)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    lines = seq(open(args.input).readlines()).map(_.call('rstrip'))

    line_level = []
    level_pre = -1
    spaces_pre = ''
    for line in lines:
        if not any([re.match(r'^\s*[-\*] .*', line), re.match(r'^\s*[0-9]\.', line)]):
            level_pre = -1
            line_level.append((line, -1, None))
            continue

        def get_movement(pre, cur):
            diff = cur - pre
            if diff > 0:
                return 1
            elif diff == 0:
                return 0
            else:
                return cur - pre

        spaces_cur = re.sub(r'^([\s]*).*', r'\g<1>', line)
        level_cur = 0
        if level_pre == -1:
            level_cur = 0
        else:
            level_cur = level_pre + get_movement(int(len(spaces_pre) / 4), int(len(spaces_cur) / 4))
        line_content = None
        item_no = None
        if re.match('^\s*[0-9]\..*', line):
            line_content = re.sub(r'^\s*[0-9]*\. (.*)', r'\g<1>', line)
            item_no = re.sub(r'^\s*([0-9])*\..*', r'\g<1>', line)
        else:
            line_content = re.sub(r'^\s*[-\*] (.*)', r'\g<1>', line)
        line_level.append((line_content, level_cur, item_no))
        level_pre = level_cur
        spaces_pre = spaces_cur

    f_out = args.output if args.output == sys.stdout else open(args.output, 'w')
    for line_content, level, item_no in line_level:
        if level < 0:
            print(line_content, file=f_out)
        else:
            itemization_mark = None
            if item_no is not None:
                itemization_mark = item_no + '.'
            else:
                itemization_mark = '*' if level % 2 == 0 else '-'
            print(''.join(['    '] * level) + itemization_mark + ' ' + line_content, file=f_out)
    f_out.close()

if __name__ == "__main__":
    main()
