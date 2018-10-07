import sys


def tracer(frame, event, arg):
    '''
        frame: スタックフレーム。実行中のコード、行番号、ローカル変数(書き込み可能)へのアクセスができる。
        event: call(関数呼び出し), line(行実行), return(関数から戻る), のいずれか。
        arg: returnイベントの戻り値。
    '''
    code = frame.f_code
    filename = code.co_filename
    function = code.co_name
    line = frame.f_lineno
    print('== ' + filename + ':' + str(line) + ' ' + function + '():', event, arg)
    return tracer


def sum_loop():
    accum = 0
    for i in range(0, 10):
        accum += i
    return accum


sys.settrace(tracer)
a = 1
accum = sum_loop()
accum += 1
accum += 1
