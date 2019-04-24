# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals


class Stack:

    def __init__(self, items=None):
        if items is None:
            items = []
        self.items = items

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def push_batch(self, items):
        self.items.extend(items)

    def pop(self):
        return self.items.pop()

    def pop_batch(self, size=99999999999):
        ret = []
        for i in range(0, size):
            if self.is_empty():
                return ret
            ret.append(self.pop())
        return ret

    def peek(self):
        return self.top()

    def top(self):
        return self.items[len(self.items) - 1]

    def top_batch(self, size=99999999999):
        return self.items[- size:][::-1]

    def size(self):
        return len(self.items)

    def __len__(self):
        return len(self.items)
