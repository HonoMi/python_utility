# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import subprocess
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', '-c')
    parser.add_argument('--save_file', '-save')
    parser.add_argument('--args_to_monitor', '-a', type=str,
                        default='', help='arg1 arg2 arg3 ..')
    args = parser.parse_args()
    return args


def get_arg_dict(args_str):
    '''
        args_str : "--arg0 hoge -a1 fuga .."
    '''
    arg_dict = {}
    i = 0
    words = args_str.rstrip().split()
    while i < len(words):
        if not words[i][0] == '-':
            i += 1
            continue
        if i + 1 < len(words):
            if words[i + 1][0] == '-':
                arg_dict[words[i].lstrip('-')] = True
                i += 1
            else:
                arg_dict[words[i].lstrip('-')] = words[i + 1]
                i += 2
        else:
            arg_dict[words[i].lstrip('-')] = True
            i += 1
    return arg_dict


def execute(args, skip=False):
    mode_str = 'skip' if skip else 'execute'
    print('\n-- online.py ' + mode_str + '! --')
    print('monitored arguments : ' + args.args_to_monitor)
    print('command : ' + args.command)
    sys.stdout.flush()
    if not skip:
        ret = subprocess.call(args.command, shell=True)
        if ret == 0:  # success
            open(args.save_file, 'a').write(args.command + '\n')
    print('-- online.py end!     --\n')


def main():
    '''
        Skip executing the command when the monitored arguments with the same values have been executed before.
    '''
    args = get_args()
    command_arg_dict = get_arg_dict(args.command)
    args_to_monitor = args.args_to_monitor.split()

    if len(args_to_monitor) == 0:
        execute(args)
        return
    if any([arg not in command_arg_dict for arg in args_to_monitor]):
        execute(args)
        return
    subprocess.call('touch ' + args.save_file, shell=True)
    for line in open(args.save_file, 'r'):
        passed_arg_dict = get_arg_dict(line.rstrip())
        if any([arg not in passed_arg_dict for arg in args_to_monitor]):
            continue
        if all([command_arg_dict[arg] == passed_arg_dict[arg] for arg in args_to_monitor]):
            execute(args, skip=True)
            return

    execute(args)
    return

if __name__ == "__main__":
    main()
