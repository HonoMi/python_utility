#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


def pdb_module_with_custom_input_channel(input_func=input):
    import imp
    import sys
    cmd_back = sys.modules.pop('cmd')
    pdb_back = sys.modules.pop('pdb')

    imp.acquire_lock()

    # 以下３行、可換でない。cmdのinputを書き換えてから、pdbからcmdをimportしたいので。
    cmd_module_with_custom_input = imp.load_module('cmd', *imp.find_module('cmd'))
    cmd_module_with_custom_input.input = input_func
    pdb_with_custom_input = imp.load_module('pdb', *imp.find_module('pdb'))

    def restore_module(module_name, backup_module):
        if backup_module is None:     # もともと無かった。
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = backup_module

    restore_module('cmd', cmd_back)
    restore_module('pdb', pdb_back)

    imp.release_lock()

    return pdb_with_custom_input


def create_command_generator(commands=['n', 'n', 'l', 'n', 'n', 'n', 'n', 'n']):
    for command in commands:
        yield command


def create_input_from_generator_func():
    command_generator = create_command_generator()

    def input_from_generator(prompt='[in]: '):
        try:
            command = command_generator.__next__()
        except StopIteration:
            command = 'exit'
        print(prompt + command)
        return command

    return input_from_generator


def test_pdb_creation():
    import pdb
    import cmd

    input_from_generator_func = create_input_from_generator_func()
    my_pdb = pdb_module_with_custom_input_channel(input_func=input_from_generator_func)

    assert(id(pdb) != id(my_pdb))
    assert(id(cmd) != id(my_pdb.cmd))
    assert(my_pdb.cmd.input == input_from_generator_func)


def pdb_debug():
    input_from_generator_func = create_input_from_generator_func()
    my_pdb = pdb_module_with_custom_input_channel(input_func=input_from_generator_func)

    my_pdb.set_trace()
    a = 1
    a = 2
    a = 3
    a = 4
    print(a)


if __name__ == '__main__':
    test_pdb_creation()
    pdb_debug()
