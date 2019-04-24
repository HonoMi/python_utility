# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# class NotCorrespondingStartStopError(Exception):
#     pass


class RunTimer:
    '''
    '''

    def __init__(self, annual_report_policy={'policy': 'call_interval', 'interval': 1}):
        self._activated = False
        self._start_times = {}
        self._stop_times = {}
        self._hit_counts = defaultdict(int)
        self._accumulated_elap_times_millisec = defaultdict(float)
        self._on_lap_flags = defaultdict(bool)
        self._report = {}

        self._annual_report_policy = annual_report_policy
        self._annual_report_memo = {'_report_is_firsttime': True}

    def _return_None_if_not_activated(func):
        def inner(self, *args, **kargs):
            if self._activated is not True:
                return None
            return func(self, *args, **kargs)
        return inner

    def activate(self):
        self._activated = True

    def set_annual_report_policy(self, annual_report_policy):
        self._annual_report_policy = annual_report_policy

    @_return_None_if_not_activated
    def lap_start(self, tag):
        if self._on_lap_flags[tag] is True:
            logger.warn('Non-pair lap_start() and lap_end() called.')
            # raise NotCorrespondingStartStopError('lap_start() and lap_end() must be called with pair.')
        self._hit_counts[tag] += 1
        self._start_times[tag] = time.time()
        self._on_lap_flags[tag] = True

    @_return_None_if_not_activated
    def lap_stop(self, tag):
        if self._on_lap_flags[tag] is False:
            logger.warn('Non-pair lap_start() and lap_end() called.')
            # raise NotCorrespondingStartStopError('lap_start() and lap_end() must be called with pair.')
        self._stop_times[tag] = time.time()

        elap_time_millisec = (self._stop_times[tag] - self._start_times[tag]) * 1000.
        self._accumulated_elap_times_millisec[tag] += elap_time_millisec
        self._on_lap_flags[tag] = False

    @_return_None_if_not_activated
    def get_report(self):
        self._update_report()
        return self._report

    @_return_None_if_not_activated
    def get_annual_report(self):
        self._update_report()
        if self._annual_report_or_not():
            return self._report
        else:
            return None

    def _update_report(self):
        tags = [tag for tag in self._stop_times]
        for tag in tags:
            spent_time = self._accumulated_elap_times_millisec[tag]
            hit_count = self._hit_counts[tag]
            per_hit = spent_time / hit_count if hit_count != 0 else -1
            self._report[tag] = {'time': spent_time, 'hits': hit_count, 'per_hit': per_hit}

    def _annual_report_or_not(self):
        if self._annual_report_policy is None:
            return True
        if self._annual_report_memo.get('_report_is_firsttime'):
            self._annual_report_memo['_report_is_firsttime'] = False
            self._annual_report_memo['num_called'] = 0
            self._annual_report_memo['time_last_called'] = time.time()
            return True

        self._annual_report_memo['num_called'] += 1
        now = time.time()
        elapsed_millisec = (now - self._annual_report_memo['time_last_called']) * 1000
        if self._annual_report_policy.get('policy') == 'call_interval':
            interval_in_num_call = self._annual_report_policy.get('interval')
            if self._annual_report_memo['num_called'] % interval_in_num_call == 0:
                return True
        elif self._annual_report_policy.get('policy') == 'time_interval':
            interval_millisec = self._annual_report_policy.get('interval')
            if elapsed_millisec > interval_millisec:
                self._annual_report_memo['time_last_called'] = now
                return True
        return False
