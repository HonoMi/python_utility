from __future__ import print_function
from __future__ import unicode_literals
import codecs
import sys

stdout_original = sys.stdout
sys.stdout = codecs.lookup('utf_8')[-1](sys.stdout)
# stdin_original = sys.stdin
# UTF8Reader = codecs.getreader('utf8')
# sys.stdin = UTF8Reader(sys.stdin)
