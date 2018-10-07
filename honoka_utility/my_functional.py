# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from functional import seq


def df2seq(df):
    from collections import namedtuple
    schema = namedtuple('MyTuple', ' '.join(df.columns))
    return seq(df).map(lambda row: schema(*row))


def seq2df(stream):
    import pandas as pd
    from collections import namedtuple
    if stream.size() == 0:
        return pd.DataFrame([])
    else:
        def is_namedtuple(obj):
            return isinstance(obj, tuple) and hasattr(obj, '_fields')
        columns = stream[0]._fields if is_namedtuple(stream[0]) else None
        return stream.to_pandas(columns=columns)
