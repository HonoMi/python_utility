# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import builtins as builtins

_tmp_dict = globals()
_use_kernprof = False


def do_nothing(func):
    return func


if isinstance(_tmp_dict["__builtins__"], dict):
    if "profile" in _tmp_dict["__builtins__"]:
        _use_kernprof = True

if not _use_kernprof:
    builtins.__dict__['profile'] = do_nothing
