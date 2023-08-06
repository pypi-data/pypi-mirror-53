from __future__ import print_function

import time
import sys
import re

from IPython.core.magics.execution import _format_time as format_delta

if sys.version_info >= (3, 3):
    _timer = time.perf_counter
elif sys.platform == 'win32':
    _timer = time.clock
else:
    _timer = time.time


class LineWatcher(object):

    """Class that implements a basic timer.

    Notes
    -----
    * Register the `start` and `stop` methods with the IPython events API.
    """

    def __init__(self):
        self.start_time = 0.0

    def start(self):
        self.start_time = _timer()

    def stop(self, result):
        raw = result.info.raw_cell
        defs_only = all(re.match('def|class|\s', line) for line in raw.split('\n'))

        if not defs_only and self.start_time:
            stop_time = _timer()
            diff = stop_time - self.start_time
            assert diff >= 0
            print('time: {}'.format(format_delta(diff)))


timer = LineWatcher()


def load_ipython_extension(ip):
    ip.events.register('pre_run_cell', timer.start)
    ip.events.register('post_run_cell', timer.stop)


def unload_ipython_extension(ip):
    ip.events.unregister('pre_run_cell', timer.start)
    ip.events.unregister('post_run_cell', timer.stop)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
