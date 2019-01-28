# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
import sys
import inspect
import functools
import chardet
import random
import string
from itertools import chain
from collections import deque
import subprocess
from collections import OrderedDict
import random
from datetime import datetime as dt
import logging
import coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


def set_logging_config(level):
    # import logging, coloredlogs
    # coloredlogs.install()
    logging.basicConfig(level=level, format='%(levelname)s %(pathname)s:%(funcName)s:%(lineno)d    %(message)s')


class ShellCommandFailedException(Exception):

    def __init__(self, message):
        self._message = message

    def __repr__(self):
        return self._message.encode('utf-8')


def exec_shell_cmd(cmd):

    def decode(data):
        auto_detected_encoding = chardet.detect(data)["encoding"]
        encoding = auto_detected_encoding if auto_detected_encoding is not None else 'utf-8'
        return data.decode(encoding)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    stdout_msg = decode(stdout_data)
    stderr_msg = decode(stderr_data)
    if p.returncode != 0:
        raise ShellCommandFailedException(stderr_msg)
    else:
        return stdout_msg, stderr_msg


# do not use "self" for a name of argument.
# [Pythonのキーワード引数も含めてmemoizeしたい - QiitaQiita](https://qiita.com/aflc/items/3a5b1f53ebaf0d9a65cc)
def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        argdict = inspect.getcallargs(obj, *args, **kwargs)
        argdict.pop('self', None)   # if obj is a bound method, arguments includes "self"
        argset = frozenset(argdict.iteritems())     # for Python3, use dict.items() instead
        if argset not in cache:
            cache[argset] = obj(*args, **kwargs)
        return cache[argset]
    return memoizer


def gzip(filename):
    os.system('gzip -f ' + filename + ' 2>/dev/null')
    return filename + '.gz'


def gzip_d(filename):
    os.system('gzip -f -d ' + filename + ' 2>/dev/null')
    return filename.rstrip('.gz')


def count_lines(filename):
    lines = 0
    for line in open(filename, 'r'):
        lines += 1
    return lines


def count_row_col(filename):
    num_row = 0
    num_col = 0
    for line in open(filename, 'r'):
        if num_row == 0:
            num_col = len(line.rstrip().split())
        num_row += 1
    return num_row, num_col


def mkdir(dir_path):
    # os.system('mkdir -p ' + dir_path)
    subprocess.call('mkdir -p ' + dir_path, shell=True)


def basename(file_path, strip_right=''):
    elems = re.split('/', file_path.rstrip())
    last_elem = elems[len(elems) - 1]
    return last_elem.rstrip(strip_right)


def dirname(file_path):
    elems = re.split('/', file_path.rstrip())
    if len(elems) == 1:
        dirpath = './'
    else:
        dirpath = '/'.join(elems[0:len(elems) - 1])
    return dirpath


def get_this_file_dir():
    return os.path.dirname(os.path.abspath(__file__))


def make_dic(filename, key_column=0, value_column=1):
    dic = OrderedDict()
    for line in open(filename, 'r'):
        if re.match('^[ \t]*#', line):  # comment line
            continue
        words = line.rstrip().split()
        dic[words[key_column]] = words[value_column]
    return dic


def is_comment_line(line):
    if re.match('^\s*#', line):
        return True
    return False


def is_blank_line(line):
    if re.match('^\s*$', line):
        return True
    return False


def is_skip_line(line):
    return is_comment_line(line) or is_blank_line(line)


def map_dic(key_list, dic, map_unk_str='as_it_is', target_column=-1, ng_word_set=set()):
    return map_dict(key_list, dic, map_unk_str=map_unk_str, target_column=target_column, ng_word_set=ng_word_set)


def map_dict(key_list, dic, map_unk_str='as_it_is', target_column=-1, ng_word_set=set()):
    dst_list = []
    for i, elem in enumerate(key_list):
        if target_column != -1 and i != target_column:
            dst_list.append(elem)
        elif elem not in dic:
            if map_unk_str == 'as_it_is':
                dst_list.append(elem)
            else:
                dst_list.append(map_unk_str)
        else:
            dst_list.append(dic[elem])
        if dst_list[-1] in ng_word_set:
            dst_list = dst_list[0:len(dst_list) - 1]
    return dst_list


def get_sublist(src_list, rmv_token_list=[], extract_token_list=[]):
    dst_list = []
    for elem in src_list:
        if elem in rmv_token_list:
            continue
        if extract_token_list != [] and elem not in extract_token_list:
            continue
        dst_list.append(elem)
    return dst_list


def run_shell_command(command, args=''):
    args_str = ' '.join(args)
    os.system(command + ' ' + args_str)


def listup_files(dir, reg_exp='.*'):
    allfiles = os.listdir(dir)
    files = []
    for file in allfiles:
        if file[0] == '.' or file[len(file) - 1] == '~':
            continue
        if not re.match(reg_exp, file):
            continue
        files.append(file)
    files_sorted = sorted(files)

    return files_sorted


def make_list(filename, key_tag=''):
    result_list = []
    for line in open(filename, 'r'):
        if key_tag == '':
            result_list.append(line.rstrip())
        else:
            fields = line.rstrip().split()
            if len(fields) < 2:
                continue
            if fields[0] == key_tag:
                result_list.append(fields[1])

    return result_list


def make_word_set(filename):
    word_set = set([])
    for line in open(filename, 'r'):
        words = line.rstrip().split()
        for word in words:
            word_set.add(word)
    return word_set


def sort_ndlist(list, key_index, elemtype_for_sort=float, reverse=False):
    return sorted(list, key=lambda x: elemtype_for_sort(x[int(key_index)]), reverse=reverse)


def split_string(str, delimiter='[ \t,:]+'):
    logger.warning('Use line.rstrip().split() insted !!')
    word_list = re.split(delimiter, str.rstrip())
    if not isinstance(word_list, list):
        word_list = [word_list]
    return word_list


def dic2list(dic):
    result_list = []
    for key in dic:
        single_raw = []
        single_raw.append(key)
        if isinstance(dic[key], list):
            for elem in dic[key]:
                single_raw.append(elem)
        else:
            single_raw.append(dic[key])
        result_list.append(single_raw)

    return result_list


def dec2hex(dec, num_fill=0):
    fill_type = '{0:0>' + str(num_fill) + '}'
    hex_str = fill_type.format(format((int)(dec), 'X'))
    return hex_str


def hex2dec(hex, num_fill=0):
    fill_type = '{0:0>' + str(num_fill) + '}'
    dec_str = fill_type.format(int('0x' + str(hex), 0))
    return dec_str


def zerofill(dec, num_fill=8):
    fill_type = '{0:0>' + str(num_fill) + '}'
    hex_str = fill_type.format((int)(dec))
    return hex_str


def open_file_read(filename):
    logger.warning('Use open!')
    return open(filename, 'r')


def open_file_write(filename):
    logger.warning('Use open!')
    return open(filename, 'w')


def read_lines_until(key_token, f_dscrpt):
    while not re.match(key_token, f_dscrpt.readline()):
        pass


def save_1dimlist(f_dscrpt, list, write_in_single_line=True):
    if write_in_single_line:
        f_dscrpt.write(' '.join(map(str, list)))
    else:
        f_dscrpt.write('\n'.join(map(str, list)))
    f_dscrpt.write('\n')


def save_2dimlist(f_dscrpt, list):
    for sub_list in list:
        f_dscrpt.write(' '.join(map(str, sub_list)) + '\n')


def save_dict(f_dscrpt, dic):
    for key in dic:
        f_dscrpt.write(key + ':' + str(dic[key]) + '\n')


def load_dict(f_dscrpt, key_type=float):
    dic = {}
    for line in f_dscrpt:
        if re.match('^$', line):
            break
        key, value = re.split('[ \t]*:[ \t]*', line)
        dic[key] = key_type(value)
    return dic


def get_time():
    tdatetime = dt.now()
    return tdatetime.strftime('%Y-%m-%d-%H-%M-%S')


def get_date():
    logger.warning('Use get_time() instead!')
    tdatetime = dt.now()
    return tdatetime.strftime('%Y-%m-%d-%H-%M-%S')


def count(filename):
    num_words = 0
    num_lines = 0
    for line in open(filename, 'r'):
        num_words += len(line.rstrip().split())
        num_lines += 1
    return num_lines, num_words


# def print_params(comment, file=sys.stdout, **param_dic):
#     print('\n', file=file)
#     print(('== ' + comment + ' =='), file=file)
#     for key, value in OrderedDict(sorted(param_dic.items())).items():
#         print((key + ' : ', value), file=file)
#     print('==', file=file)
#     sys.stdout.flush()


def dump_params(param_dic):
    params_reprs = []
    for key, value in OrderedDict(sorted(param_dic.items(), key=lambda x: str(x[0]))).items():
        params_reprs.append('{0:<25} : {1:<10}'.format(key.__repr__(), value.__repr__()))
    return '\n'.join(params_reprs)


def fill_with_space(elem, total_char=10):
    str_formatted = str(elem).ljust(total_char)
    return str_formatted


def make_tmp_dir(prefix=''):
    tmp_dir_name = prefix + '.tmp.' + dt.now().strftime('%Y-%m-%d-%H-%M-%S') + \
        str(random.randint(0, 10000))
    os.system('mkdir -p ' + tmp_dir_name)
    return tmp_dir_name


def flatten(nested_list):
    flat_list = []
    fringe = [nested_list]
    while len(fringe) > 0:
        node = fringe.pop(0)
        if isinstance(node, list):
            fringe = node + fringe
        else:
            flat_list.append(node)
    return flat_list


def numpy_address(x):
    # この関数は配列のメモリブロックアドレスを返します
    return x.__array_interface__['data'][0]


def open_(input_name='__stdin__', mode='r'):
    """
        Do not use this method without \"with\" statement.
    """
    return InputModule(input_name=input_name, mode='r')


class InputModule:

    def __init__(self, input_name='__stdin__', mode='r'):
        if mode != 'r':
            print('!! ERROR !! InputModule, mode!=\'r\' is not implemented yet.')
            return
        self.input_name = input_name
        self.mode = mode
        self.in_mod = None

    def set_in_mod(self):
        if self.in_mod is not None:
            return
        if self.input_name == '__stdin__':
            self.in_mod = sys.stdin
        else:
            self.in_mod = open(self.input_name, 'r')

    def read(self):
        self.set_in_mod()
        return self.in_mod.read()

    def readline(self):
        self.set_in_mod()
        return self.in_mod.readline()

    def readlines(self):
        self.set_in_mod()
        return self.in_mod.readlines()

    def __enter__(self):
        self.set_in_mod()
        return self.in_mod

    def __exit__(self, exception_type, exception_value, traceback):
        self.in_mod.close()


def copy_file_to_local(in_file, local_disk='/tmp', no_copy=False, print_log=True):
    full_path = subprocess.check_output('readlink -f ' + in_file, shell=True).decode().rstrip()
    file_on_local = local_disk + '/' + full_path
    mkdir(dirname(file_on_local))
    if no_copy:
        return file_on_local

    command = 'cp ' + in_file + ' ' + file_on_local
    if print_log:
        print('-- copying to local disk... --')
        print(command)
        print('-- copying to local disk end! --')

    subprocess.call(command, shell=True)
    return file_on_local


def run_jobs(jobs):
    """
        from multiprocessing import Process
        jobs = [
            Process(target=countDown, args=(n1,)),
            Process(target=countDown, args=(n2,)),
            Process(target=countDown, args=(n3,)),
            Process(target=countDown, args=(n4,)),
        ]
    """
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()


def get_file_path():
    raise NotImplementedError()
    # return os.path.dirname(os.path.realpath(__file__))


def is_comment(line):
    return re.match('^#.*', line)


def is_blank(line):
    return re.match('^[ \t]*$', line)


def filter(orig_list, filter_list):
    assert(len(orig_list) == len(filter_list))
    ret_list = []
    for elem, flag in zip(orig_list, filter_list):
        if flag:
            ret_list.append(elem)
    return ret_list


def file2list(filename):
    line_list = []
    for line in open(filename, 'r'):
        if is_comment(line) or is_blank(line):
            continue
        line_list.append(line.rstrip())
    return line_list


def get_f_out(output, option='w'):
    return open_f_out(output, option=option)


def open_f_out(output, option='w'):
    f_out = sys.stdout
    if output != sys.stdout:
        mkdir(dirname(output))
        f_out = open(output, option)
    return f_out


def get_f_in(input):
    return open_f_in(input)


def open_f_in(input):
    f_in = sys.stdin
    if input != sys.stdin:
        f_in = open(input, 'r')
    return f_in


def close_f_in(f_in):
    if f_in != sys.stdin:
        f_in.close()


def close_f_out(f_out):
    if f_out != sys.stdout:
        f_out.close()


def total_size(obj, verbose=False):
    seen = set()

    def sizeof(o):
        if id(o) in seen:
            return 0

        seen.add(id(o))
        s = sys.getsizeof(o, default=0)
        if verbose:
            print(s, type(o), repr(o))
        if isinstance(o, (tuple, list, set, frozenset, deque)):
            s += sum(map(sizeof, iter(o)))
        elif isinstance(o, dict):
            s += sum(map(sizeof, chain.from_iterable(o.items())))
        elif "__dict__" in dir(o):  # もっと良い方法はあるはず
            s += sum(map(sizeof, chain.from_iterable(o.__dict__.items())))
        return s

    return sizeof(obj)


def indent_brackets(text, indent_width=2):
    str_level_pairs = []
    level = 0
    buf = ''
    for char in text:
        if char == '(':
            str_level_pairs.append((buf + '(\n', level))
            level += 1
            buf = ''
            continue
        elif char == ')':
            if buf != '':
                str_level_pairs.append((buf + '\n', level))
            level -= 1
            str_level_pairs.append((')\n', level))
            buf = ''
            continue
        buf += char
    ret_str = ''
    for (chars, level) in str_level_pairs:
        ret_str += ''.join(''.join([' '] * indent_width) * level) + chars
    return ret_str


# def compose(outer_func, inner_func):
#     def composed(*args, **kwds):
#         return outer_func(inner_func(*args, **kwds))
#     return composed


# def compose(*funcs):
#     composed = None
#     for next_func in funcs[::-1]:
#         if composed is None:
#             def compose_2(*args, **kwds):
#                 return next_func(*args, **kwds)
#             composed = compose_2
#         else:
#             def compose_2(*args, **kwds):
#                 return next_func(composed(*args, **kwds))
#             composed = compose_2
#     return composed

def compose(*funcs):
    def composed_func(*args, **kwds):
        if len(funcs) > 1:
            ret = funcs[-1](*args, **kwds)
            for func in funcs[::-1][1:]:
                ret = func(ret)
            return ret
        else:
            return None
    return composed_func


def pipe(*funcs):
    def composed_func(*args, **kwds):
        if len(funcs) > 1:
            ret = funcs[0](*args, **kwds)
            for func in funcs[1:]:
                ret = func(ret)
            return ret
        else:
            return None
    return composed_func


def random_name(n=10):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)
